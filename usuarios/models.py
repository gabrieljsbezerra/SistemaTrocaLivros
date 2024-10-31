from django.db import models

class TabelaUsuarios(models.Model):
    nome_usuario = models.CharField(max_length=40)
    email = models.EmailField()
    senha = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Tabela_Usuario'

    def __str__(self):
        return self.nome_usuario
