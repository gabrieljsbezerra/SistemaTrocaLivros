from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('Meus Livros/', views.meus_livros, name='meus_livros'),
]