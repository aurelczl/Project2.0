from django import forms
from .models import Book, Series, Movie, Manga, Genre
import datetime

class MangaForm(forms.ModelForm):
    raw_genres = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = Manga
        fields = ['title', 'statut', 'finished_year',
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
    
class BookForm(forms.ModelForm):
    raw_genres = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'read','finished_year','finished_month','finished_day', 'edition', 'global_rate', 'image']

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
        book = super().save(commit=False)
        book.user = user
        if commit:
            book.save()

        # genres = self.cleaned_data.get('genres') ne marche plus
        genres = self.cleaned_data.get('raw_genres', [])
        book.genres.set(genres)
        return book


class SeriesForm(forms.ModelForm):
    raw_genres = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = Series
        fields = ['title', 'seasons', 'episodes', 'completed','finished_year','finished_month','finished_day', 'stop_area', 'global_rate', 'image']

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
        fields = ['title', 'director', 'watched', 'global_rate','finished_year','finished_month','finished_day', 'image', 'raw_genres']

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
