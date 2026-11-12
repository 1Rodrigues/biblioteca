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
        fields = ['titulo', 'ano_publicacao', 'disponivel', 'autor', 'categories']
