from django.shortcuts import render
from django.http import HttpResponse
from .models import TabelaUsuarios
from django.shortcuts import redirect
from hashlib import sha256
from django.urls import reverse

def login(request):
    return HttpResponse('login')


def cadastro(request):
    status = request.GET.get('status')
    if status is not None:
        status = int(status)
    return render(request, 'cadastro.html', {'status': status})


def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    usuario_existente = TabelaUsuarios.objects.filter(email=email)

    # Validação do nome e email
    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect(f"{reverse('cadastro')}?status=1")

    # Validação do tamanho da senha
    if len(senha) < 8:
        return redirect(f"{reverse('cadastro')}?status=2")

    # Verificação de usuário existente
    if len(usuario_existente) > 0:
        return redirect(f"{reverse('cadastro')}?status=3")

    try:
        # Criação de hash da senha e salvamento do usuário
        senha = sha256(senha.encode()).hexdigest()
        usuario = TabelaUsuarios(nome_usuario=nome, senha=senha, email=email)
        usuario.save()
        return redirect(f"{reverse('cadastro')}?status=0")
    except Exception as e:
        # Em caso de erro, status 4
        return redirect(f"{reverse('cadastro')}?status=4")
