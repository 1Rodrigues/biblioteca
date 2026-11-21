from django.urls import path

from . import views

urlpatterns = [
    path("", views.LivroListView.as_view(), name="listar_livros"),
    path("sobre/", views.SobreView.as_view(), name="sobre"),
    path("autor/<int:pk>/", views.AuthorDetailView.as_view(), name="author_detail"),
    path("autor/criar/", views.AuthorCreateView.as_view(), name="author_create"),
    path("livro/<int:pk>/", views.LivroDetailView.as_view(), name="livro_detail"),
    path("livro/criar/", views.LivroCreateView.as_view(), name="livro_create"),
    path("livro/<int:pk>/editar/", views.LivroUpdateView.as_view(), name="livro_edit"),
    path("livro/<int:pk>/excluir/", views.LivroDeleteView.as_view(), name="livro_delete"),
]
