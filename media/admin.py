from django.contrib import admin
from .models import Genre, PublicBook, Book, Movie, PublicManga, Manga, Series
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

"""
@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'statut', 'reading_info')
    list_filter = ('statut', 'user')
    search_fields = ('public_manga__title', 'user__username')
    raw_id_fields = ('public_manga',)

    def title(self, obj):
        return obj.public_manga.title if obj.public_manga else '-'
    title.short_description = "Titre"

    def reading_info(self, obj):
        return f"{obj.scan or '-'} | {obj.reading_website or '-'}"
    reading_info.short_description = "Scan/Site"
"""
@admin.register(PublicManga)
class PublicMangaAdmin(admin.ModelAdmin):
    """ Gestion des PublicManga depuis le superuser """
    list_display = ('title', 'user_count', 'last_updated')
    search_fields = ('title',)
    readonly_fields = ('user_count_with_list', 'image_preview')
    
    def save_model(self, request, obj, form, change):
        obj._from_admin = True  # Marque comme venant de l'admin
        super().save_model(request, obj, form, change)
    
    def user_count(self, obj):
        return obj.mangas.count()  # Utilisation du related_name 'mangas'
    user_count.short_description = "Utilisateurs"

    def user_count_with_list(self, obj):
        count = obj.mangas.count()
        if count == 0:
            return "Aucun utilisateur"
        
        users = obj.mangas.select_related('user').all()[:10]
        user_list = ", ".join([manga.user.username for manga in users])
        
        if count > 10:
            user_list += f" (+{count - 10} autres)"
            
        return format_html(
            '<span title="{}" style="cursor:help; border-bottom:1px dotted #999;">{} utilisateurs</span>',
            user_list,
            count
        )
    user_count_with_list.short_description = "Utilisateurs (liste)"

    def last_updated(self, obj):
        last = obj.mangas.order_by('-id').first()
        return last.user.username if last else '-'
    last_updated.short_description = "Dernier ajout"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:200px;"/>',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Aperçu"
