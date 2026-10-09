from django.shortcuts import render, get_object_or_404
from .models import Book, Author

# Create your views here.
def listar_livros(request):
    lista_de_livros = Book.objects.all()
    return render(request, 'lista_livros.html', {'lista_de_livros': lista_de_livros})

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    context = {'author': author}
    return render(request,'author_detail.html' ,context)
