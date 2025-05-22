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

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    read = models.BooleanField(default=False)
    genres = models.ManyToManyField(Genre, blank=True)
    finished_year = models.PositiveIntegerField(blank=True, null=True)
    finished_month = models.PositiveIntegerField(blank=True, null=True)
    finished_day = models.PositiveIntegerField(blank=True, null=True)
    edition = models.CharField(max_length=100, blank=True)
    global_rate = models.IntegerField(validators=[MinValueValidator(0),
                                                  MaxValueValidator(100)],
                                      null=True,blank=True,default=0,
                                      help_text="Note entre 0 et 100")
    if RENDER:
        upload_path = ''  # Cloudinary n’utilise pas vraiment ce chemin
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
    completed = models.BooleanField(default=False)
    finished_year = models.PositiveIntegerField(blank=True, null=True)
    finished_month = models.PositiveIntegerField(blank=True, null=True)
    finished_day = models.PositiveIntegerField(blank=True, null=True)

    stop_area = models.CharField(max_length=100, blank=True, null=True)
    global_rate = models.IntegerField(validators=[MinValueValidator(0),
                                                  MaxValueValidator(100)],
                                      null=True,blank=True,default=0,
                                      help_text="Note entre 0 et 100")
    #global_rate = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True, default=0)
    genres = models.ManyToManyField(Genre, blank=True)
    if RENDER:
        upload_path = ''  # Cloudinary n’utilise pas vraiment ce chemin
    else:
        upload_path = 'series_images/'
    image = models.ImageField(upload_to=upload_path, blank=True, null=True)

    def __str__(self):
        return self.title

class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    director = models.CharField(max_length=100)
    watched = models.BooleanField(default=False)
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
        upload_path = ''  # Cloudinary n’utilise pas vraiment ce chemin
    else:
        upload_path = 'movie_images/'
    image = models.ImageField(upload_to=upload_path, blank=True, null=True)
    
    def __str__(self):
        return self.title
