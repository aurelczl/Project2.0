from django.contrib import admin
from .models import Genre, PublicBook, Book, Movie, Manga, Series
from django.utils.html import format_html
# Register your models here.

admin.site.register(Genre)

# Version2.0 : bib à deux niveau BOOK 

admin.site.register(Book)

@admin.register(PublicBook)
class PublicBookAdmin(admin.ModelAdmin):
    """ Gestion des public book depuis le superuser"""
    list_display = ('title', 'author', 'edition', 'user_count')
    search_fields = ('title', 'author')
    list_filter = ('edition',)
    readonly_fields = ('user_count_with_list',)

    def save_model(self, request, obj, form, change):
        obj._from_admin = True  # Marque comme venant de l'admin
        super().save_model(request, obj, form, change)
    
    def user_count(self, obj):
        return obj.books.count()  # <-- Utilisez le related_name ici
    user_count.short_description = "Utilisateurs"

    def user_count_with_list(self, obj):
        count = obj.books.count()
        if count == 0:
            return "Aucun utilisateur"
        
        users = obj.books.select_related('user').all()[:10]  # Limite à 10 utilisateurs
        user_list = ", ".join([book.user.username for book in users])
        
        if count > 10:
            user_list += f" (+{count - 10} autres)"
            
        return format_html(
            '<span title="{}" style="cursor:help; border-bottom:1px dotted #999;">{} utilisateurs</span>',
            user_list,
            count
        )
    user_count_with_list.short_description = "Utilisateurs (liste)"

admin.site.register(Movie)
admin.site.register(Series)
admin.site.register(Manga)
