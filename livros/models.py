from django.db import models
from datetime import date

class TabelaCategorias(models.Model):
    nome_categoria = models.CharField(max_length=30)
    descricao = models.CharField(max_length=60)

    class Meta:
        verbose_name = 'Tabela_Categoria'

    def __str__(self):
        return self.nome_categoria



class TabelaLivros(models.Model):
    nome_livro = models.CharField(max_length=100)
    autor = models.CharField(max_length=50)
    co_autor = models.CharField(max_length=50, blank=True, null=True)
    editora = models.CharField(max_length=30)
    categoria = models.ForeignKey(TabelaCategorias, on_delete=models.DO_NOTHING)
    braile = models.BooleanField(default=False)
    data_cadastro = models.DateField(default=date.today)

    class Meta:
        verbose_name = 'Tabela_Livro'

    def __str__(self):
        return self.nome_livro
