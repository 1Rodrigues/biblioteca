from django.core.validators import FileExtensionValidator, MaxValueValidator, MinLengthValidator, MinValueValidator, RegexValidator
from django.db import models

from .validators import validar_ano_publicacao, validar_tamanho_arquivo

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
    titulo = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    ano_publicacao = models.IntegerField(validators=[validar_ano_publicacao])
    paginas = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5000)])
    isbn = models.CharField(
        max_length=13, blank=True,
        validators=[RegexValidator(r"^\d{13}$", "O ISBN deve ter exatamente 13 dígitos.")])
    capa = models.ImageField(
        upload_to="capas/", blank=True,
        validators=[validar_tamanho_arquivo,
                    FileExtensionValidator(["jpg", "jpeg", "png"])])
    disponivel = models.BooleanField(default=True)
    authors = models.ManyToManyField(Author, related_name='books')
    categories = models.ManyToManyField(Category, null = True, blank=True)

    def __str__(self):
        return self.titulo


