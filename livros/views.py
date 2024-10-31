from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
from usuarios.models import TabelaUsuarios


def home(request):
    if request.session.get('usuarios'):
        usuario = TabelaUsuarios.objects.get(
            id=request.session['usuarios']).nome_usuario
        return HttpResponse(f'Olá, {usuario}')
    else:
        return redirect(f"{reverse('login')}?status=2")
