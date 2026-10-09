from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50, null = True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["name"]
        verbose_name_plural = 'Autores'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Categories'

class Book(models.Model):
    titulo = models.CharField(max_length=200)
    ano_publicacao = models.IntegerField()
    disponivel = models.BooleanField(default=True)
    autor = models.ForeignKey(Author, null = True, on_delete=models.SET_NULL, related_name='books')
    categories = models.ManyToManyField(Category, null = True, blank=True)

    def __str__(self):
        return self.titulo


