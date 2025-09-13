from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from asgiref.sync import async_to_sync
from django import forms
from .models import Simulation, Project, Paper



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
    }
    return render(request, 'literature_search.html', context)


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

    paper_form = PaperForm(instance=paper)
    return render(request, 'projects_detail.html', {
        'project': project,
        'paper': paper,
        'paper_form': paper_form,
        'experiments': experiments,
        'citations': citations,
    })


@login_required
def projects_update_paper(request, pk: int):
    project = Project.objects.get(pk=pk, owner=request.user)
    paper = Paper.objects.get(project=project)
    if request.method == 'POST':
        form = PaperForm(request.POST, instance=paper)
        if form.is_valid():
            form.save()
    return redirect('projects_detail', pk=project.pk)
