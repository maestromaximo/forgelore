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
    path('experiments/', views.experiments_list, name='experiments_list'),
    path('experiments/new/', views.experiments_create, name='experiments_create'),
    path('experiments/<int:pk>/', views.experiments_detail, name='experiments_detail'),
    path('experiments/<int:pk>/run/', views.experiments_run, name='experiments_run'),
]

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
    path('experiments/', views.experiments_list, name='experiments_list'),
    path('experiments/new/', views.experiments_create, name='experiments_create'),
    path('experiments/<int:pk>/', views.experiments_detail, name='experiments_detail'),
    path('experiments/<int:pk>/run/', views.experiments_run, name='experiments_run'),
]