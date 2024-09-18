from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Set home as the default path
    # Other URLs...
]
