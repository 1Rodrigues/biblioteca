from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import CriarAuthor, CriarBook
from .models import Author, Book


# Create your views here.
class LivroListView(ListView):
    model = Book
    template_name = "lista_livros.html"
    context_object_name = "lista_de_livros"

    def get_queryset(self):
        return Book.objects.order_by("titulo")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lista_de_autores"] = Author.objects.all()
        return context


class LivroDetailView(DetailView):
    model = Book
    template_name = "livro_detail.html"
    context_object_name = "livro"


class LivroCreateView(CreateView):
    model = Book
    form_class = CriarBook
    template_name = "livro_create.html"
    success_url = reverse_lazy("listar_livros")


class LivroUpdateView(UpdateView):
    model = Book
    form_class = CriarBook
    template_name = "livro_create.html"
    context_object_name = "livro"
    success_url = reverse_lazy("listar_livros")


class LivroDeleteView(DeleteView):
    model = Book
    template_name = "livro_confirm_delete.html"
    context_object_name = "livro"
    success_url = reverse_lazy("listar_livros")


class AuthorDetailView(DetailView):
    model = Author
    template_name = "author_detail.html"


class AuthorCreateView(CreateView):
    model = Author
    form_class = CriarAuthor
    template_name = "author_create.html"

    def get_success_url(self):
        return reverse("author_detail", kwargs={"pk": self.object.pk})


class SobreView(TemplateView):
    template_name = "sobre.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = Book.objects.count()
        context["disponiveis"] = Book.objects.filter(disponivel=True).count()
        return context
