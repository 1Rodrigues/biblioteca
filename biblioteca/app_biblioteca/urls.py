from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListBooksView.as_view(), name = 'listar_livros'),
    path('autor/<int:pk>/', views.AutorDetailView.as_view(), name = 'author_detail'),
    path('cadastrar_autor/', views.AutorCreateView.as_view(), name='cadastrar_autor'),
    path('cadastrar_livro/', views.BookCreateView.as_view(), name='cadastrar_livro'),
    path('editar_autor/<int:pk>/', views.AutorUpdateView.as_view(), name='editar_autor'),
    path('editar_livro/<int:pk>/', views.BookUpdateView.as_view(), name='editar_livro'),
]
