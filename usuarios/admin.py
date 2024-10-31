from django.contrib import admin
from .models import TabelaUsuarios

@admin.register(TabelaUsuarios)
class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields = ('nome_usuario', 'email', 'senha')