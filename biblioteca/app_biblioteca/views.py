from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Author
from .forms import AuthorForm, ModelBookForm
# Create your views here.
def listar_livros(request):
    lista_de_livros = Book.objects.all()
    return render(request, 'lista_livros.html', {'lista_de_livros': lista_de_livros})

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    context = {'author': author}
    return render(request,'author_detail.html' ,context)

def cadastrar_autor(request, pk = None):
    author = None
    if pk:
        author = get_object_or_404(Author, pk=pk)

    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            author = form.save()
            return redirect('author_detail', pk=author.pk)
    else:
        form = AuthorForm(instance=author)
    return render(request, 'cadastrar_autor.html', {'form': form, 'autor': author})

def cadastrar_livro(request, pk = None):
    livro = None
    if pk:
        livro = get_object_or_404(Book, pk = pk)
    if request.method == 'POST':
        form = ModelBookForm(request.POST, instance = livro)
        if form.is_valid():
            livro = form.save()
            return redirect('author_detail', pk = livro.autor.pk)
    else:
        form = ModelBookForm(instance = livro)
    return render(request, 'cadastrar_livro.html', {'form': form, 'livro': livro})
