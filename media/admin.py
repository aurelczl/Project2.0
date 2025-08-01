from django.contrib import admin
from .models import Genre, PublicBook, Book, Movie, Manga, Series

# Register your models here.

admin.site.register(Genre)

# Version2.0 : bib à deux niveau BOOK 

#admin.site.register(PublicBook)
admin.site.register(Book)

@admin.register(PublicBook)
class PublicBookAdmin(admin.ModelAdmin):
    """ Gestion des public book depuis le superuser"""
    list_display = ('title', 'author', 'edition', 'user_count')
    search_fields = ('title', 'author')
    list_filter = ('edition',)

    def save_model(self, request, obj, form, change):
        obj._from_admin = True  # Marque comme venant de l'admin
        super().save_model(request, obj, form, change)
    
    def user_count(self, obj):
        return obj.books.count()  # <-- Utilisez le related_name ici
    user_count.short_description = "Utilisateurs"

admin.site.register(Movie)
admin.site.register(Series)
admin.site.register(Manga)
