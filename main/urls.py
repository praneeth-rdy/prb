# Django Imports
from django.urls import path, include

# Standard Package Imports

# Project Imports
from . import views


# Third Party Imports


app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('register-tasks', views.register_tasks, name='tasks'),
    path('send-notices', views.send_notices, name='send_notices'),
    # path('get_quote/', views.get_quote, name='get_quote'),
    # path('<int:year>/', views.diary),
    # path('<int:year>/<str:name>/', views.diary),
]