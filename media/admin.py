from django.contrib import admin
from .models import Genre, PublicBook, Book, Movie, Manga, Series

# Register your models here.

admin.site.register(Genre)
# Version2.0
admin.site.register(PublicBook)
admin.site.register(Book)
# Version 1.0 
"""
admin.site.register(Book)
"""
admin.site.register(Movie)
admin.site.register(Series)
admin.site.register(Manga)
