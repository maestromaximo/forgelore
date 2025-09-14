from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('literature/search/', views.literature_search, name='literature_search'),
    path('literature/link/<int:project_pk>/', views.literature_link_to_project, name='literature_link_to_project'),
    path('experiments/', views.experiments_list, name='experiments_list'),
    path('experiments/new/', views.experiments_create, name='experiments_create'),
    path('experiments/<int:pk>/', views.experiments_detail, name='experiments_detail'),
    path('experiments/<int:pk>/run/', views.experiments_run, name='experiments_run'),
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/new/', views.projects_create, name='projects_create'),
    path('projects/<int:pk>/', views.projects_detail, name='projects_detail'),
    path('projects/<int:pk>/assistant/chat/', views.project_chat, name='project_chat'),
    path('projects/<int:pk>/paper/update/', views.projects_update_paper, name='projects_update_paper'),
    path('projects/<int:pk>/paper/recompile/', views.projects_recompile_paper, name='projects_recompile_paper'),
    path('projects/<int:pk>/notes/add/', views.projects_add_note, name='projects_add_note'),
    path('projects/<int:pk>/hypotheses/add/', views.projects_add_hypothesis, name='projects_add_hypothesis'),
    path('projects/<int:pk>/automation/status/', views.project_automation_status, name='project_automation_status'),
    path('api/transcribe/', views.transcribe_audio, name='transcribe_audio'),
]