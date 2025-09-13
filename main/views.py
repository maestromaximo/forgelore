from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from asgiref.sync import async_to_sync
from django import forms
from .models import Simulation, Project



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
