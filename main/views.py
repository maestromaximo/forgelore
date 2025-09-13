from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect


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
