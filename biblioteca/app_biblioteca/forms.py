from django import forms
from .models import Book, Author


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'nationality']
        labels = {
            'name': 'Nome',
            'nationality': 'Nacionalidade',
        }

class ModelBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['titulo', 'autor', 'ano_publicacao', 'disponivel', 'categories', 'paginas','isbn','capa',]
        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'ano_publicacao': 'Ano de publicação',
            'disponivel': 'Disponível',
            'categories': 'Categorias',
            'paginas': 'Páginas',
        }
        widgets = {
            'categories': forms.CheckboxSelectMultiple,
        }

    '''def clean_titulo(self):
        titulo = ' '.join(self.cleaned_data['titulo'].split())
        if len(titulo) < 3:
            raise forms.ValidationError('O título precisa ter pelo menos 3 caracteres, sem contar os espaços extras.')
        return titulo'''

    '''def clean_ano_publicacao(self):
        ano = self.cleaned_data['ano_publicacao']
        ano_atual = timezone.localdate().year
        if ano > ano_atual:
            raise forms.ValidationError(f'O ano não pode ser maior que {ano_atual}. Informe o ano em que o livro foi publicado.')
        return ano'''
