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
        usuario = TabelaUsuarios.objects.get(id=request.session['usuarios'])
        livros = TabelaLivros.objects.filter(usuario = usuario)
        return render(request, 'meus_livros.html', {'livros': livros})
    else:
        return redirect(f"{reverse('login')}?status=2")
    
def procura_livros(request):
    if request.session.get('usuarios'):
        usuario = TabelaUsuarios.objects.get(id=request.session['usuarios'])
        query = request.GET.get('q', '')  # Obtém o termo de pesquisa

        # Filtra os livros do usuário atual com base no termo de pesquisa
        procura_livros = TabelaLivros.objects.filter(
            Q(nome_livro__icontains=query) | 
            Q(autor__icontains=query) | 
            Q(editora__icontains=query),
            usuario=usuario  # Restringe aos livros do usuário logado
        ) if query else TabelaLivros.objects.filter(usuario=usuario)

        return render(request, 'meus_livros.html', {'livros': procura_livros, 'query': query})
    else:
        return redirect(f"{reverse('login')}?status=2")

def ver_livro(request, id):
    if request.session.get('usuarios'):
        livro = TabelaLivros.objects.get(id=id)
        if request.session.get('usuarios') == livro.usuario.id:
            return render(request, 'ver_livro.html', {'livro':livro})
        else:
            return redirect(f"{reverse('home')}?status=1")
    else:
        return redirect(f"{reverse('login')}?status=2")

def editar_livro(request, id):
    if request.session.get('usuarios'):
        livro = TabelaLivros.objects.get(id=id)
        categorias = TabelaCategorias.objects.all()
        if request.session.get('usuarios') == livro.usuario.id:
            return render(request, 'editar_livro.html', {'livro': livro, 'categorias': categorias})
        else:
            return redirect(f"{reverse('home')}?status=1")
    else:
        return redirect(f"{reverse('login')}?status=2")

def alterar_livro(request, id):
    pass


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
