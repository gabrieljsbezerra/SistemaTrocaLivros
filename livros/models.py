from django.db import models
from datetime import date


class TabelaLivros(models.Model):
    nome_livro = models.CharField(max_length=100)
    autor = models.CharField(max_length=50)
    co_autor = models.CharField(max_length=50, blank=True, null=True)
    editora = models.CharField(max_length=30)
    cateoria = models.CharField(max_length=30)
    braile = models.BooleanField(default=False)
    data_cadastro = models.DateField(default=date.today)

    class Meta:
        verbose_name = 'Tabela_Livro'