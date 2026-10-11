from django.contrib import admin
from .models import Book, Author, Category

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    fields = ["titulo", "authors", "ano_publicacao", "disponivel", "categories"]
    list_display = ["titulo", "autores", "ano_publicacao", "disponivel"]
    search_fields = ["titulo", "authors__name"]
    list_filter = ["disponivel", "categories"]

    filter_horizontal = ["authors", "categories"]

    @admin.display(description="Autores")
    def autores(self, obj):
        return ", ".join(author.name for author in obj.authors.all())


class BookInline(admin.TabularInline):
    model = Book.authors.through
    extra = 1


class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
