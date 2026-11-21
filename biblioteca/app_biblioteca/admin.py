from django.contrib import admin
from .models import Book, Author, Category

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    fields = ["titulo", "autor", "ano_publicacao", "disponivel", "categories","paginas","isbn","capa"]  # adicionado "capa" para poder enviar pelo admin
    list_display = ["titulo", "autor", "ano_publicacao", "disponivel"]
    search_fields = ["titulo", "autor__name"]
    list_filter = ["disponivel", "categories"]

    filter_horizontal = ["categories"]

class BookInline(admin.TabularInline):
    model = Book
    fields = ["titulo", "ano_publicacao", "disponivel", "categories", "paginas","isbn","capa"]  # adicionado "capa" no inline do autor também
    filter_horizontal = ["categories"]
    extra = 1

class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
