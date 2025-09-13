from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from asgiref.sync import async_to_sync
from django import forms
from django.db.models import Q
from .models import Simulation, Project, Paper, Hypothesis, Note, Literature, Citation, LiteratureSourceType



def home(request):
    """Landing page using templates/home.html."""
    return render(request, 'home.html')


@login_required
def dashboard(request):
    """Dashboard overview using templates/dashboard.html."""
    return render(request, 'dashboard.html')


def signup(request):
    """User registration with auto-login, redirects to dashboard."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def literature_search(request):
    """Synchronous wrapper view that runs async provider searches and renders results.

    Query via GET param `q`. Shows grouped results by source.
    """
    query = request.GET.get('q', '').strip()
    selected_project_id = request.GET.get('project') or None
    user_projects = Project.objects.filter(owner=request.user).order_by('name')
    results_by_source = None
    error = None
    if query:
        from .research_services import HttpClient, search_all

        def _run():
            async def go():
                client = HttpClient()
                try:
                    mailto = request.GET.get('mailto') or None
                    return await search_all(client, query=query, limit_per_source=10, mailto=mailto)
                finally:
                    await client.aclose()

            return async_to_sync(go)()

        try:
            results_by_source = _run()
        except Exception as exc:
            error = str(exc)

    context = {
        'query': query,
        'results_by_source': results_by_source,
        'error': error,
        'projects': user_projects,
        'selected_project_id': int(selected_project_id) if selected_project_id else None,
    }
    return render(request, 'literature_search.html', context)


@login_required
def literature_link_to_project(request, project_pk: int):
    """Create or update a Literature entry from posted search result payload and link to the project's paper as a Citation.

    Expected POST fields (best-effort, many optional): title, url, doi, arxiv_id, open_access_pdf_url, year, authors (comma-separated), venue, abstract
    """
    project = Project.objects.get(pk=project_pk, owner=request.user)
    paper, _ = Paper.objects.get_or_create(project=project, defaults={'title': project.name, 'abstract': project.abstract})
    if request.method == 'POST':
        title = (request.POST.get('title') or '').strip() or 'Untitled'
        doi = (request.POST.get('doi') or '').strip()
        arxiv_id = (request.POST.get('arxiv_id') or '').strip()
        url = (request.POST.get('url') or '').strip() or (request.POST.get('open_access_pdf_url') or '').strip()
        year = request.POST.get('year') or None
        abstract = request.POST.get('abstract') or ''
        authors_list = (request.POST.get('authors') or '').strip()
        venue = (request.POST.get('venue') or '').strip()

        # Heuristic: prefer DOI, then arXiv id, else title+url
        lit_q = Literature.objects.all()
        if doi:
            lit_q = lit_q.filter(doi=doi)
        elif arxiv_id:
            lit_q = lit_q.filter(arxiv_id=arxiv_id)
        else:
            lit_q = lit_q.filter(title=title, url=url)

        literature = lit_q.first()
        if not literature:
            literature = Literature.objects.create(
                title=title,
                authors=authors_list,
                journal_or_publisher=venue,
                year=int(year) if (year and year.isdigit()) else None,
                doi=doi,
                arxiv_id=arxiv_id,
                url=url,
                source_type=LiteratureSourceType.DOI if doi else (LiteratureSourceType.ARXIV if arxiv_id else LiteratureSourceType.URL),
                abstract=abstract,
            )

        # Link to paper via Citation (append to end)
        last_order = paper.citations.aggregate_max = paper.citations.order_by('-order').first().order if paper.citations.exists() else 0
        Citation.objects.create(paper=paper, literature=literature, order=last_order + 1)

        # Redirect back to literature search, preserving q and project selection
        q = request.GET.get('q') or ''
        return redirect(f"/literature/search/?q={q}&project={project.pk}")
    return redirect('literature_search')


class SimulationForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = [
            'project', 'paper', 'hypothesis', 'name', 'description', 'code', 'language', 'parameters'
        ]


@login_required
def experiments_list(request):
    sims = Simulation.objects.filter(project__owner=request.user).order_by('-created_at')
    return render(request, 'experiments_list.html', {"simulations": sims})


@login_required
def experiments_create(request):
    if request.method == 'POST':
        form = SimulationForm(request.POST)
        if form.is_valid():
            sim = form.save()
            return redirect('experiments_detail', pk=sim.pk)
    else:
        # Limit project choices to the user's own projects
        form = SimulationForm()
        form.fields['project'].queryset = Project.objects.filter(owner=request.user)
    return render(request, 'experiments_create.html', {"form": form})


@login_required
def experiments_detail(request, pk: int):
    sim = Simulation.objects.get(pk=pk, project__owner=request.user)
    return render(request, 'experiments_detail.html', {"simulation": sim})


@login_required
def experiments_run(request, pk: int):
    sim = Simulation.objects.get(pk=pk, project__owner=request.user)
    sim.run(timeout_seconds=30)
    return redirect('experiments_detail', pk=sim.pk)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'abstract', 'description']


class PaperForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ['title', 'abstract', 'content_raw', 'content_format']


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'body', 'pinned']


class HypothesisForm(forms.ModelForm):
    class Meta:
        model = Hypothesis
        fields = ['title', 'statement']


@login_required
def projects_list(request):
    projects = Project.objects.filter(owner=request.user).order_by('-updated_at')
    return render(request, 'projects_list.html', {'projects': projects})


@login_required
def projects_create(request):
    class ProjectUploadForm(ProjectForm):
        paper_file = forms.FileField(required=False, help_text="Optional. Upload a .pdf or .txt paper draft.")

    def extract_text(file) -> str:
        name = getattr(file, 'name', '') or ''
        if name.lower().endswith('.txt'):
            return file.read().decode('utf-8', errors='ignore')
        # Fallback to PDF
        try:
            from pypdf import PdfReader
            reader = PdfReader(file)
            pages = []
            for page in reader.pages:
                try:
                    pages.append(page.extract_text() or '')
                except Exception:
                    continue
            return "\n\n".join(pages)
        except Exception:
            return ""

    if request.method == 'POST':
        form = ProjectUploadForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()

            # Create or update the associated paper
            paper = Paper.objects.create(project=project, title=project.name, abstract=project.abstract)

            uploaded = form.cleaned_data.get('paper_file')
            if uploaded:
                full_text = extract_text(uploaded)
                # Placeholder: set first chars to abstract/description
                snippet = (full_text or '')[:500]
                paper.abstract = snippet[:300]
                paper.content_raw = full_text
                paper.save(update_fields=['abstract', 'content_raw', 'updated_at'])
                if not project.abstract:
                    project.abstract = paper.abstract
                if not project.description:
                    project.description = snippet
                project.save(update_fields=['abstract', 'description', 'updated_at'])

            return redirect('projects_detail', pk=project.pk)
    else:
        form = ProjectUploadForm()
    return render(request, 'projects_create.html', {'form': form})


@login_required
def projects_detail(request, pk: int):
    project = Project.objects.get(pk=pk, owner=request.user)
    # Ensure paper exists (safety)
    paper, _ = Paper.objects.get_or_create(project=project, defaults={'title': project.name, 'abstract': project.abstract})

    experiments = Simulation.objects.filter(project=project).order_by('-updated_at')[:10]
    citations = paper.citations.select_related('literature').order_by('order')
    hypotheses = Hypothesis.objects.filter(project=project).order_by('-updated_at')
    notes = project.notes.all()
    related_literature = Literature.objects.filter(
        Q(citations__paper=paper) | Q(hypotheses__project=project)
    ).distinct().order_by('-updated_at')

    paper_form = PaperForm(instance=paper)
    note_form = NoteForm()
    hypothesis_form = HypothesisForm()
    initial_tab = request.GET.get('tab') or 'overview'
    return render(request, 'projects_detail.html', {
        'project': project,
        'paper': paper,
        'paper_form': paper_form,
        'experiments': experiments,
        'citations': citations,
        'hypotheses': hypotheses,
        'notes': notes,
        'related_literature': related_literature,
        'note_form': note_form,
        'hypothesis_form': hypothesis_form,
        'initial_tab': initial_tab,
    })


@login_required
def projects_update_paper(request, pk: int):
    project = Project.objects.get(pk=pk, owner=request.user)
    paper = Paper.objects.get(project=project)
    if request.method == 'POST':
        form = PaperForm(request.POST, instance=paper)
        if form.is_valid():
            form.save()
    tab = request.GET.get('tab') or request.POST.get('tab') or 'paper'
    return redirect(f"/projects/{project.pk}/?tab={tab}")


@login_required
def projects_add_note(request, pk: int):
    project = Project.objects.get(pk=pk, owner=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.project = project
            note.save()
    return redirect(f"/projects/{project.pk}/?tab=notes")


@login_required
def projects_add_hypothesis(request, pk: int):
    project = Project.objects.get(pk=pk, owner=request.user)
    if request.method == 'POST':
        form = HypothesisForm(request.POST)
        if form.is_valid():
            hyp = form.save(commit=False)
            hyp.project = project
            # By default, tie to the project's paper if present
            try:
                hyp.paper = project.paper
            except Paper.DoesNotExist:
                pass
            hyp.save()
    return redirect(f"/projects/{project.pk}/?tab=hypotheses")
