from django.contrib import admin
from . models import TabelaLivros, TabelaCategorias, TabelaTrocas

#Registrando minhas tabelas na parte administrativa
admin.site.register(TabelaLivros)

admin.site.register(TabelaCategorias)

admin.site.register(TabelaTrocas)
