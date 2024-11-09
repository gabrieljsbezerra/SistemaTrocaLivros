from django import forms
from .models import TabelaLivros


class CadastroLivro(forms.ModelForm):
    class Meta:
        model = TabelaLivros
        fields = ['nome_livro', 'autor', 'co_autor', 'editora', 'categoria',
                  'braile', 'imagem_link', 'imagem_upload', 'data_cadastro']
        widgets = {
            'imagem_link': forms.URLInput(attrs={'id': 'imagemLink', 'placeholder': 'Insira o link da imagem'}),
            'imagem_upload': forms.FileInput(attrs={'id': 'imagemUpload', 'accept': 'image/*'}),
        }

from django import forms
from .models import TabelaLivros

class CadastroLivro(forms.ModelForm):
    class Meta:
        model = TabelaLivros
        fields = ['nome_livro', 'autor', 'co_autor', 'editora', 'categoria', 'braile', 'imagem_link', 'imagem_upload']
        widgets = {
            'nome_livro': forms.TextInput(attrs={'class': 'input-custom', 'placeholder': 'Nome do Livro'}),
            'autor': forms.TextInput(attrs={'class': 'input-custom', 'placeholder': 'Autor'}),
            'co_autor': forms.TextInput(attrs={'class': 'input-custom', 'placeholder': 'Co-Autor'}),
            'editora': forms.TextInput(attrs={'class': 'input-custom', 'placeholder': 'Editora'}),
            'imagem_link': forms.URLInput(attrs={'class': 'input-custom', 'placeholder': 'URL da Imagem'}),
            'imagem_upload': forms.FileInput(attrs={'class': 'form-control'}),
        }
