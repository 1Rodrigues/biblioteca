from django.urls import path

from . import views

urlpatterns = [
    path("", views.listar_livros, name="listar_livros"),
    path("autor/<int:pk>/", views.author_detail, name="author_detail"),
    path("autor/criar/", views.author_create, name="author_create"),
    path("livro/criar/", views.livro_form, name="livro_create"),
    path("livro/<int:pk>/editar/", views.livro_form, name="livro_edit"),
]
