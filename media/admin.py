from django.contrib import admin
from .models import Genre, Book, Movie, Series

# Register your models here.

admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Movie)
admin.site.register(Series)
