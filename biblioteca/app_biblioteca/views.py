from django.shortcuts import get_object_or_404, redirect, render

from .forms import CriarAuthor, CriarBook
from .models import Author, Book


# Create your views here.
def listar_livros(request):
    lista_de_livros = Book.objects.all()
    lista_de_autores = Author.objects.all()
    context = {"lista_de_livros": lista_de_livros, "lista_de_autores": lista_de_autores}
    return render(request, "lista_livros.html", context)


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    context = {"author": author}
    return render(request, "author_detail.html", context)


def author_create(request):
    if request.method == "POST":
        form = CriarAuthor(request.POST)
        if form.is_valid():
            novo_autor = form.save()
            return redirect("author_detail", pk=novo_autor.id)
    else:
        form = CriarAuthor()

    context = {"form": form}
    return render(request, "author_create.html", context)


def livro_form(request, pk=None):
    livro = get_object_or_404(Book, pk=pk) if pk else None

    if request.method == "POST":
        form = CriarBook(request.POST, request.FILES, instance=livro)
        if form.is_valid():
            livro = form.save()
            return redirect("author_detail", pk=livro.authors.first().pk)
    else:
        form = CriarBook(instance=livro)

    context = {"form": form, "livro": livro}
    return render(request, "livro_create.html", context)
