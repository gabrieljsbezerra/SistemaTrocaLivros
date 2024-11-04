from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
from usuarios.models import TabelaUsuarios
from .models import TabelaLivros, TabelaCategorias
from . import forms
from django.db.models import Q
from datetime import date
from django.contrib import messages


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

def ver_livro(request, id):
    livro = TabelaLivros.objects.get(id=id)
    return render(request, 'ver_livro.html', {'livro':livro})
    
def cadastro_livro(request):
    status = request.GET.get('status')
    if status is not None:
        status = int(status)
    categorias = TabelaCategorias.objects.all()
    return render(request, 'cadastro_livro.html', {'status': status, 'categorias': categorias})

from django.shortcuts import render, redirect, get_object_or_404
from .models import TabelaLivros, TabelaCategorias
from usuarios.models import TabelaUsuarios
from django.contrib import messages
from datetime import date

def valida_cadastro_livro(request):
    if request.method == "POST":
        # Obtenha os dados do formulário
        nome_livro = request.POST.get("nome")
        autor = request.POST.get("autor")
        editora = request.POST.get("editora")
        categoria_id = request.POST.get("categoria")
        braile = request.POST.get("braile", False)
        imagem_link = request.POST.get("imagem_link")
        imagem_upload = request.FILES.get("imagem_upload")
        
        # Obtenha o usuário logado na tabela TabelaUsuarios
        try:
            usuario = TabelaUsuarios.objects.get(id=request.user.id)
        except TabelaUsuarios.DoesNotExist:
            messages.error(request, "Usuário inválido.")
            return redirect("cadastro_livro")

        # Verifique se a categoria existe
        try:
            categoria = TabelaCategorias.objects.get(id=categoria_id)
        except TabelaCategorias.DoesNotExist:
            messages.error(request, "Categoria inválida.")
            return redirect("cadastro_livro")

        # Validação dos campos obrigatórios
        if not nome_livro or not autor or not editora or not categoria_id:
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return redirect("cadastro_livro")

        # Crie o objeto do livro
        livro = TabelaLivros(
            nome_livro=nome_livro,
            autor=autor,
            editora=editora,
            categoria=categoria,
            braile=braile,
            data_cadastro=date.today(),
            usuario=usuario,
            imagem_link=imagem_link,
            imagem_upload=imagem_upload,
        )

        # Tente salvar o livro no banco de dados
        try:
            livro.save()
            messages.success(request, "Livro cadastrado com sucesso!")
            return redirect("meus_livros")  # Redireciona para a página de "Meus Livros"
        except Exception as e:
            messages.error(request, f"Erro ao cadastrar o livro: {e}")
            return redirect("cadastro_livro")
    else:
        return redirect("cadastro_livro")
