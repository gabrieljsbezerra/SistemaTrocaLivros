from django import forms
from .models import TabelaLivros

class LivroForm(forms.ModelForm):
    class Meta:
        model = TabelaLivros
        fields = ['nome_livro', 'autor', 'co_autor', 'editora', 'categoria', 'braile', 'imagem_link', 'imagem_upload']
        widgets = {
            'imagem_link': forms.URLInput(attrs={'placeholder': 'Insira o link da imagem'}),
            'imagem_upload': forms.FileInput(attrs={'accept': 'image/jpeg'}),
        }