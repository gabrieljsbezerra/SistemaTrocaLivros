from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
from usuarios.models import TabelaUsuarios
from .models import TabelaLivros
from django.db.models import Q


def home(request):
    if request.session.get('usuarios'):
        usuario = TabelaUsuarios.objects.get(id=request.session['usuarios']).nome_usuario
        livros = TabelaLivros.objects.all()
        return render(request, 'home.html', {'livros':livros})
        
    else:
        return redirect(f"{reverse('login')}?status=2")
    
def meus_livros(request):
    if request.session.get('usuarios'):
        usuario = TabelaUsuarios.objects.get(id=request.session['usuarios']).nome_usuario
        query = request.GET.get('q', '')  # Obtém o termo de pesquisa

        # Filtra os livros com base no termo de pesquisa
        livros = TabelaLivros.objects.filter(
            Q(nome_livro__icontains=query) | 
            Q(autor__icontains=query) | 
            Q(editora__icontains=query)
        ) if query else TabelaLivros.objects.all()

        return render(request, 'meus_livros.html', {'livros': livros, 'query': query})
    else:
        return redirect(f"{reverse('login')}?status=2")
        