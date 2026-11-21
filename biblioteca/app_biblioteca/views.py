from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, DetailView, CreateView, UpdateView
from .models import Book, Author
from .forms import AuthorForm, ModelBookForm
# Create your views here.

'''def listar_livros(request):
    lista_de_livros = Book.objects.all()
    return render(request, 'lista_livros.html', {'lista_de_livros': lista_de_livros})'''

class ListBooksView(ListView):
    model = Book
    template_name = 'lista_livros.html'
    context_object_name = 'lista_de_livros'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_disponiveis"] = Book.objects.all().filter(disponivel=True).count()
        return context



''''def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    context = {'author': author}
    return render(request,'author_detail.html' ,context)'''

class AutorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'

class AutorCreateView(CreateView):
    model = Author
    template_name = 'cadastrar_autor.html'
    form_class = AuthorForm
    def get_success_url(self) -> str:
        return reverse_lazy('author_detail', kwargs = {'pk': self.object.pk})

class AutorUpdateView(UpdateView):
    model = Author
    template_name = 'cadastrar_autor.html'
    form_class = AuthorForm
    context_object_name = 'autor'
    success_url = reverse_lazy('listar_livros')

'''def cadastrar_autor(request, pk = None):
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
    return render(request, 'cadastrar_autor.html', {'form': form, 'autor': author})'''


'''def cadastrar_livro(request, pk = None):
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
    return render(request, 'cadastrar_livro.html', {'form': form, 'livro': livro})'''

class BookCreateView(CreateView):
    model = Book
    template_name = 'cadastrar_livro.html'
    form_class = ModelBookForm
    success_url = reverse_lazy('listar_livros')

class BookUpdateView(UpdateView):
    model = Book
    template_name = 'cadastrar_livro.html'
    form_class = ModelBookForm
    context_object_name = 'livro'
    success_url = reverse_lazy('listar_livros')

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'livro_confirm_delete.html'
    context_object_name = 'livro'
    success_url = reverse_lazy('listar_livros')


