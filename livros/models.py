from django.db import models
from datetime import date
from usuarios.models import TabelaUsuarios
from django.contrib.auth.models import User


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
    categoria = models.ForeignKey(
        'TabelaCategorias', on_delete=models.DO_NOTHING)
    braile = models.BooleanField(default=False)
    data_cadastro = models.DateField(default=date.today)
    usuario = models.ForeignKey(TabelaUsuarios, on_delete=models.DO_NOTHING)
    imagem_link = models.URLField(blank=True, null=True)
    imagem_upload = models.ImageField(
        upload_to='livros_imagens/', blank=True, null=True)
    disponivel_para_troca = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Tabela_Livro'

    def __str__(self):
        return self.nome_livro


class TabelaTrocas(models.Model):
    livro_oferecido = models.ForeignKey(
        TabelaLivros, related_name='trocas_oferecidas', on_delete=models.CASCADE
    )
    livro_solicitado = models.ForeignKey(
        TabelaLivros, related_name='trocas_solicitadas', on_delete=models.CASCADE
    )
    usuario_oferecedor = models.ForeignKey(
        TabelaUsuarios, related_name='trocas_oferecidas_por_usuario', on_delete=models.CASCADE
    )
    usuario_solicitante = models.ForeignKey(
        TabelaUsuarios, related_name='trocas_solicitadas_por_usuario', on_delete=models.CASCADE
    )
    data_proposta = models.DateField(default=date.today)
    status = models.CharField(
        max_length=20,
        choices=[('Pendente', 'Pendente'), ('Aceita', 'Aceita'),
                 ('Rejeitada', 'Rejeitada')],
        default='Pendente'
    )

    class Meta:
        verbose_name = 'Tabela_Troca'

    def __str__(self):
        return f"{self.livro_oferecido} <-> {self.livro_solicitado}"


class Troca(models.Model):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Aceita', 'Aceita'),
        ('Rejeitada', 'Rejeitada')
    ]

    usuario_solicitante = models.ForeignKey(
        TabelaUsuarios, on_delete=models.CASCADE, related_name='trocas_solicitantes'
    )
    usuario_dono = models.ForeignKey(
        TabelaUsuarios, on_delete=models.CASCADE, related_name='trocas_dono_livro'
    )
    livro_solicitado = models.ForeignKey(
        TabelaLivros, on_delete=models.CASCADE, related_name='livros_solicitados'
    )
    livro_oferecido = models.ForeignKey(
        TabelaLivros, on_delete=models.CASCADE, related_name='livros_oferecidos'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pendente'
    )

    def __str__(self):
        return f"{self.usuario_solicitante} solicitou troca do livro {self.livro_solicitado.nome_livro} (Status: {self.status})"
