from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from .models import Book, PublicBook, Series, Movie, Manga, Genre
import datetime

class MangaForm(forms.ModelForm):
    raw_genres = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = Manga
        fields = ['title', 'statut', 'scan', 'reading_website', 'finished_year',
                  'finished_month','finished_day',
                  'global_rate', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        year = cleaned_data.get('finished_year')
        month = cleaned_data.get('finished_month')
        day = cleaned_data.get('finished_day')

        if day and (not month or not year):
            raise forms.ValidationError("Si vous indiquez un jour, le mois et l’année doivent aussi être renseignés.")
        if month and not year:
            raise forms.ValidationError("Si vous indiquez un mois, l’année doit être renseignée.")

        # Optionnel : vérifier que la date est valide
        if year and month and day:
            try:
                datetime.date(year, month, day)
            except ValueError:
                raise forms.ValidationError("La date saisie n'est pas valide.")

        return cleaned_data
    
    def clean_global_rate(self):
        rate = self.cleaned_data.get('global_rate')
        if rate is not None and (rate < 0 or rate > 100):
            raise ValidationError("La note doit être comprise entre 0 et 100.")
        return rate
    
    def clean_raw_genres(self):
        raw = self.cleaned_data.get('raw_genres', '')
        names = [name.strip() for name in raw.split(',') if name.strip()]
        genres = []
        for name in names:
            genre, _ = Genre.objects.get_or_create(name=name)
            genres.append(genre)
        return genres

    def save(self, user, commit=True):
        manga = super().save(commit=False)
        manga.user = user
        if commit:
            manga.save()

        # genres = self.cleaned_data.get('genres') ne marche plus
        genres = self.cleaned_data.get('raw_genres', [])
        manga.genres.set(genres)
        return manga

""" 
Création form book pour la version 2.0 
composé de public et user book : Version 1.0 à commenter
"""
# Version 2.0 

class BookForm(forms.ModelForm):
    raw_genres = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    # Déclarez explicitement les champs de PublicBook comme champs de formulaire
    title = forms.CharField(max_length=200)
    author = forms.CharField(max_length=100, required=False)
    edition = forms.CharField(max_length=100, required=False)
    pageCount = forms.IntegerField(
        required=False,
        validators=[MinValueValidator(0), MaxValueValidator(10000)]
    )
    image = forms.ImageField(required=False)

    class Meta:
        model = Book
        fields = ['statut', 'finished_year', 'finished_month', 'finished_day', 'global_rate']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Pré-remplir les valeurs si instance existe
        if self.instance.pk:
            self.fields['title'].initial = self.instance.public_book.title
            self.fields['author'].initial = self.instance.public_book.author
            self.fields['edition'].initial = self.instance.public_book.edition
            self.fields['pageCount'].initial = self.instance.public_book.pageCount
            self.fields['image'].initial = self.instance.public_book.image

    def clean(self):
        cleaned_data = super().clean()
        year = cleaned_data.get('finished_year')
        month = cleaned_data.get('finished_month')
        day = cleaned_data.get('finished_day')

        if day and (not month or not year):
            raise forms.ValidationError("Si vous indiquez un jour, le mois et l’année doivent aussi être renseignés.")
        if month and not year:
            raise forms.ValidationError("Si vous indiquez un mois, l’année doit être renseignée.")

        # Optionnel : vérifier que la date est valide
        if year and month and day:
            try:
                datetime.date(year, month, day)
            except ValueError:
                raise forms.ValidationError("La date saisie n'est pas valide.")

        return cleaned_data
    
    def clean_global_rate(self):
        rate = self.cleaned_data.get('global_rate')
        if rate is not None and (rate < 0 or rate > 100):
            raise ValidationError("La note doit être comprise entre 0 et 100.")
        return rate
    
    def clean_raw_genres(self):
        raw = self.cleaned_data.get('raw_genres', '')
        names = [name.strip() for name in raw.split(',') if name.strip()]
        genres = []
        for name in names:
            genre, _ = Genre.objects.get_or_create(name=name)
            genres.append(genre)
        return genres

    def save(self, commit=True):
        # Créer/mettre à jour PublicBook d'abord
        public_book, created = PublicBook.objects.get_or_create(
            title=self.cleaned_data['title'],
            defaults={
                'author': self.cleaned_data['author'],
                'edition': self.cleaned_data['edition'],
                'pageCount': self.cleaned_data['pageCount'],
                'image': self.cleaned_data.get('image')
            }
        )
        
        if not created:
            # Mettre à jour les champs si le livre existait déjà
            public_book.author = self.cleaned_data['author']
            public_book.edition = self.cleaned_data['edition']
            public_book.pageCount = self.cleaned_data['pageCount']
            if self.cleaned_data.get('image'):
                public_book.image = self.cleaned_data['image']
            public_book.save()

        # Créer/mettre à jour Book
        book = super().save(commit=False)
        book.user = self.user
        book.public_book = public_book
        
        if commit:
            book.save()
            self.save_m2m()

        # Gestion des genres
        genres = self.cleaned_data.get('raw_genres', [])
        if genres:
            book.genres.set(genres)
        
        return book

class SeriesForm(forms.ModelForm):
    raw_genres = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = Series
        fields = ['title', 'seasons', 'episodes',# 'completed',
        'finished_year','finished_month','finished_day',
         'statut', 'saison', 'episode', 'global_rate', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_global_rate(self):
        rate = self.cleaned_data.get('global_rate')
        if rate is not None and (rate < 0 or rate > 100):
            raise ValidationError("La note doit être comprise entre 0 et 100.")
        return rate
    
    def clean_raw_genres(self):
        raw = self.cleaned_data.get('raw_genres', '')
        names = [name.strip() for name in raw.split(',') if name.strip()]
        genres = []
        for name in names:
            genre, _ = Genre.objects.get_or_create(name=name)
            genres.append(genre)
        return genres

    def save(self, user, commit=True):
        serie = super().save(commit=False)
        serie.user = user
        if commit:
            serie.save()
            serie.genres.set(self.cleaned_data.get('raw_genres', []))
        return serie

    
class MovieForm(forms.ModelForm):
    raw_genres = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Movie
        fields = ['title', 'director','statut', # 'watched',
         'global_rate','finished_year','finished_month','finished_day',
          'image', 'raw_genres']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            existing = ','.join([g.name for g in self.instance.genres.all()])
            self.fields['raw_genres'].initial = existing

    def clean_global_rate(self):
        rate = self.cleaned_data.get('global_rate')
        if rate is not None and (rate < 0 or rate > 100):
            raise ValidationError("La note doit être comprise entre 0 et 100.")
        return rate
    
    def clean_raw_genres(self):
        raw = self.cleaned_data.get('raw_genres', '')
        names = [name.strip() for name in raw.split(',') if name.strip()]
        genres = []
        for name in names:
            genre, _ = Genre.objects.get_or_create(name=name)
            genres.append(genre)
        return genres

    def save(self, user, commit=True):
        movie = super().save(commit=False)
        movie.user = user
        if commit:
            movie.save()
            self.save_m2m()

        # assign genres
        genres = self.cleaned_data.get('raw_genres', [])
        if genres:
            movie.genres.set(genres)
        else:
            movie.genres.clear()

        return movie
