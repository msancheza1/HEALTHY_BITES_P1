from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('progress/', views.progress_history, name='progress_history'),
]