from django.db import models
from django.core.validators import MinLengthValidator,  MinValueValidator, MaxValueValidator, RegexValidator, FileExtensionValidator
from .validators import ValidarAnoPublicacao, ValidarTamanhoCapa

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
    titulo = models.CharField(max_length=200, validators=[MinLengthValidator(3,'o titulo deve ter pelo menos 3 caracteres')])
    ano_publicacao = models.IntegerField(validators=[ValidarAnoPublicacao])
    disponivel = models.BooleanField(default=True)
    autor = models.ForeignKey(Author, null = True, on_delete=models.SET_NULL, related_name='books')
    categories = models.ManyToManyField(Category, null = True, blank=True)
    paginas = models.IntegerField(null=True, blank = True, validators = [MinValueValidator(1,'o livro deve ter pelo menos uma pagina'), MaxValueValidator(5000, 'o maximo de poaginas é de 5000')])
    isbn = models.CharField(null=True, blank=True, validators = [RegexValidator(r'^\d{13}$','o isbn deve ter exatamente 13 dígitos')])
    capa = models.FileField(upload_to='capas/',blank=True, null = True, validators=[FileExtensionValidator(['jpeg','png','jpg'],'O arquivo deve ser uma imagem(png, jpg ou jpeg)'), ValidarTamanhoCapa])

    def __str__(self):
        return self.titulo


