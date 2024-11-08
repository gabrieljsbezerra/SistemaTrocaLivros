from django.db import models
from datetime import date
from usuarios.models import TabelaUsuarios

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
    usuario = models.ForeignKey(TabelaUsuarios, on_delete=models.DO_NOTHING)
    imagem_link = models.URLField(blank=True, null=True)  # Link da imagem
    imagem_upload = models.ImageField(upload_to='livros_imagens/', blank=True, null=True) # Upload da imagem

    class Meta:
        verbose_name = 'Tabela_Livro'

    def __str__(self):
        return self.nome_livro

class TabelaTrocas(models.Model):
    livro_oferecido = models.ForeignKey(TabelaLivros, related_name='livro_oferecido', on_delete=models.CASCADE)
    livro_solicitado = models.ForeignKey(TabelaLivros, related_name='livro_solicitado', on_delete=models.CASCADE)
    usuario_oferecedor = models.ForeignKey(TabelaUsuarios, related_name='usuario_oferecedor', on_delete=models.CASCADE)
    usuario_solicitante = models.ForeignKey(TabelaUsuarios, related_name='usuario_solicitante', on_delete=models.CASCADE)
    data_proposta = models.DateField(default=date.today)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pendente', 'Pendente'),
            ('Aceita', 'Aceita'),
            ('Rejeitada', 'Rejeitada'),
            ('Concluída', 'Concluída')
        ],
        default='Pendente'
    )

    class Meta:
        verbose_name = 'Tabela_Troca'

    def __str__(self):
        return f"{self.livro_oferecido} <-> {self.livro_solicitado}"