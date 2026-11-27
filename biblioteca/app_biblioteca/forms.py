from datetime import date

from django import forms

from .models import Author, Book


class CriarAuthor(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "nationality"]
        labels = {
            "name": "Nome do Autor",
            "nationality": "Nacionalidade",
        }


class CriarBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["titulo", "authors", "ano_publicacao", "disponivel", "categories", "paginas", "isbn", "capa"]

        labels = {
            "titulo": "Título",
            "authors": "Autores",
            "ano_publicacao": "Ano de publicação",
            "disponivel": "Disponível",
            "categories": "Categorias",
            "paginas": "Páginas",
            "isbn": "ISBN",
            "capa": "Capa",
        }
        widgets = {
            "categories": forms.CheckboxSelectMultiple(),
        }

    def clean_titulo(self):
        titulo = " ".join(self.cleaned_data["titulo"].split())
        if len(titulo) < 3:
            raise forms.ValidationError(
                "O título precisa ter pelo menos 3 caracteres (sem contar espaços extras). "
                "Digite um título mais longo."
            )
        return titulo

    def clean_ano_publicacao(self):
        ano = self.cleaned_data["ano_publicacao"]
        ano_atual = date.today().year
        if ano > ano_atual:
            raise forms.ValidationError(
                f"O ano de publicação não pode ser posterior a {ano_atual}. "
                f"Informe um ano até {ano_atual}."
            )
        return ano
