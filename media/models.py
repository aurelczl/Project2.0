from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

import os
from cloudinary.models import CloudinaryField

RENDER = os.getenv('RENDER', 'False').lower() == 'true'

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Manga(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, blank=True)
    statuts = {
        "Fini": "Fini",
        "Arrêté": "Arrêté",
        "En cours": "En cours",
        "En attente": "En attente",
    }
    statut = models.CharField( max_length=10, choices=statuts, blank=True, null=True)
    scan = models.CharField(max_length=2000, blank=True, null=True)
    reading_website = models.URLField(blank=True, null=True)
    finished_year = models.PositiveIntegerField(blank=True, null=True)
    finished_month = models.PositiveIntegerField(blank=True, null=True)
    finished_day = models.PositiveIntegerField(blank=True, null=True)
    global_rate = models.IntegerField(validators=[MinValueValidator(0),
                                                  MaxValueValidator(100)],
                                      null=True,blank=True,default=0,
                                      help_text="Note entre 0 et 100")
    if RENDER:
        image = CloudinaryField("image", blank=True, null=True)
    else:
        upload_path = 'manga_images/'
        image = models.ImageField(upload_to=upload_path, blank=True, null=True)

    def __str__(self):
        return self.title
    
class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, blank=True, null=True)
    #read = models.BooleanField(default=False)
    statuts = {
        "Fini": "Fini",
        "Arrêté": "Arrêté",
        "En cours": "En cours",
        "En attente": "En attente",
    }
    statut = models.CharField( max_length=10, choices=statuts, blank=True, null=True)
    genres = models.ManyToManyField(Genre, blank=True)
    finished_year = models.PositiveIntegerField(blank=True, null=True)
    finished_month = models.PositiveIntegerField(blank=True, null=True)
    finished_day = models.PositiveIntegerField(blank=True, null=True)
    edition = models.CharField(max_length=100, blank=True)
    pageCount =  models.IntegerField(validators=[MinValueValidator(0),
                                                  MaxValueValidator(10000)],
                                      null=True,blank=True)
    global_rate = models.IntegerField(validators=[MinValueValidator(0),
                                                  MaxValueValidator(100)],
                                      null=True,blank=True,default=0,
                                      help_text="Note entre 0 et 100")
    if RENDER:
        image = CloudinaryField("image", blank=True, null=True)
    else:
        upload_path = 'book_images/'
        image = models.ImageField(upload_to=upload_path, blank=True, null=True)

    def __str__(self):
        return self.title

class Series(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    seasons = models.PositiveIntegerField()
    episodes = models.PositiveIntegerField(blank=True, null=True)
    #completed = models.BooleanField(default=False)
    finished_year = models.PositiveIntegerField(blank=True, null=True)
    finished_month = models.PositiveIntegerField(blank=True, null=True)
    finished_day = models.PositiveIntegerField(blank=True, null=True)
    statuts = {
        "Fini": "Fini",
        "Arrêté": "Arrêté",
        "En cours": "En cours",
        "En attente": "En attente",
    }
    statut = models.CharField( max_length=10, choices=statuts, blank=True, null=True)
    saison = models.CharField(max_length=25, blank=True, null=True)
    episode = models.CharField(max_length=100, blank=True, null=True)
    global_rate = models.IntegerField(validators=[MinValueValidator(0),
                                                  MaxValueValidator(100)],
                                      null=True,blank=True,default=0,
                                      help_text="Note entre 0 et 100")
    #global_rate = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True, default=0)
    genres = models.ManyToManyField(Genre, blank=True)
    if RENDER:
        image = CloudinaryField("image", blank=True, null=True)
    else:
        upload_path = 'series_images/'
        image = models.ImageField(upload_to=upload_path, blank=True, null=True)

    def __str__(self):
        return self.title

class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    director = models.CharField(max_length=100, blank=True, null=True)
    #watched = models.BooleanField(default=False)
    statuts = {
        "Fini": "Fini",
        "Arrêté": "Arrêté",
        "En attente": "En attente",
    }
    statut = models.CharField( max_length=10, choices=statuts, blank=True, null=True)
    finished_year = models.PositiveIntegerField(blank=True, null=True)
    finished_month = models.PositiveIntegerField(blank=True, null=True)
    finished_day = models.PositiveIntegerField(blank=True, null=True)
    genres = models.ManyToManyField(Genre, blank=True)
    global_rate = models.IntegerField(validators=[MinValueValidator(0),
                                                  MaxValueValidator(100)],
                                      null=True,blank=True,default=0,
                                      help_text="Note entre 0 et 100")
    #global_rate = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True, default=0) 
    if RENDER:
        image = CloudinaryField("image", blank=True, null=True)
    else:
        upload_path = 'movie_images/'
        image = models.ImageField(upload_to=upload_path, blank=True, null=True)
    
    def __str__(self):
        return self.title
