from django.urls import path
from . import views


urlpatterns = [
    path('', views.listar_livros, name = 'listar_livros'),
    path('autor/<int:pk>/', views.author_detail, name = 'author_detail'),
    path('cadastrar_autor/', views.cadastrar_autor, name='cadastrar_autor'),
    path('cadastrar_livro/', views.cadastrar_livro, name='cadastrar_livro'),
    path('editar_autor/<int:pk>/', views.cadastrar_autor, name='editar_autor'),
    path('editar_livro/<int:pk>/', views.cadastrar_livro, name='editar_livro'),
]
