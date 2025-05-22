from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, Series, Movie, Manga, Genre
from .forms import BookForm, SeriesForm, MovieForm, MangaForm
from django.http import Http404, JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q
import json

# Gestion des données local pour render :

@csrf_exempt
def load_data(request):
    if request.method == 'POST':
        try:
            from django.core.management import call_command
            call_command('loaddata', 'data.json')
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        
# Create your views here.

def home(request):
    return render(request, 'media/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion auto après inscription
            return redirect('profile')  # on ira à la page profil ensuite
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def library_view(request):
    books = Book.objects.filter(user=request.user)
    series = Series.objects.filter(user=request.user)
    movies = Movie.objects.filter(user=request.user)
    mangas = Manga.objects.filter(user=request.user)

    return render(request, 'media/library.html', {
        'books': books,
        'series': series,
        'movies': movies,
        'mangas': mangas,
    })

@login_required
def edit_item(request, model_name, item_id):
    model_mapping = {
        'book': Book,
        'movie': Movie,
        'series': Series,
        'manga': Manga,
    }

    model_class = model_mapping.get(model_name.lower())
    if not model_class:
        return redirect('home')

    item = get_object_or_404(model_class, id=item_id, user=request.user)

    form_class = {
        Book: BookForm,
        Movie: MovieForm,
        Series: SeriesForm,
        Manga: MangaForm
    }.get(model_class)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(user=request.user)
            return redirect('item_detail', model_name=model_name, item_id=item.id)
    else:
        form = form_class(instance=item)
        form.initial['raw_genres'] = ','.join([g.name for g in item.genres.all()])

    return render(request, 'media/edit_item.html', {
        'form': form,
        'title': f"Modifier : {item.title}",
        'all_genres': Genre.objects.all(),
    })

def delete_item(request, model_name, item_id):
    model_mapping = {
        'book': Book,
        'movie': Movie,
        'series': Series,
        'manga': Manga,
    }

    model_class = model_mapping.get(model_name.lower())
    if not model_class:
        raise Http404("Type inconnu")

    item = get_object_or_404(model_class, id=item_id, user=request.user)
    
    # Supprimer l'élément
    item.delete()
    
    # Rediriger vers la page de profil après suppression
    return redirect('profile')


def add_genre(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Genre.objects.get_or_create(name=name)
        return redirect('add_book')  # ou une autre vue
    return render(request, 'media/add_genre.html')

def search(request):
    query = request.GET.get('q', '')
    content_type = request.GET.get('type', 'all')

    books = movies = series = []
    
    print("on utilise la fonction search de view")
    
    if query:
        if content_type == 'book' or content_type == 'all':
            books = Book.objects.filter(
                Q(title__icontains=query) | Q(author__icontains=query),
                user=request.user
            )
        if content_type == 'movie' or content_type == 'all':
            movies = Movie.objects.filter(
                Q(title__icontains=query) | Q(director__icontains=query),
                user=request.user
            )
        if content_type == 'series' or content_type == 'all':
            series = Series.objects.filter(
                Q(title__icontains=query) | Q(director__icontains=query),
                user=request.user
            )

    context = {
        'query': query,
        'books': books,
        'movies': movies,
        'series': series,
    }
    return render(request, 'media/search_results.html', context)

@login_required
def profile(request):
    books = Book.objects.filter(user=request.user)
    series = Series.objects.filter(user=request.user)
    movies = Movie.objects.filter(user=request.user)
    mangas = Manga.objects.filter(user=request.user)
    all_genres = Genre.objects.all()
    
    num_books = books.count()
    num_series = series.count()
    num_movies = movies.count()
    num_mangas = mangas.count()

    all_items = list(books) + list(movies) + list(series)+ list(mangas)

    # Ajoute un attribut model_name à chaque item
    for book in books:
        book.model_name = 'book'
    for serie in series:
        serie.model_name = 'series'
    for movie in movies:
        movie.model_name = 'movie'
    for manga in mangas:
        manga.model_name = 'manga'

    # Calculer une taille max basée sur la note (global_rate), min 50px max 150px
    for item in all_items:
        rate = getattr(item, 'global_rate', 100)
        if rate is None:
            rate = 100
        rate = int(rate)
        # Clamp entre 50 et 150 px
        item.display_size = max(50, min(rate, 180))
        
    return render(request, 'media/profile.html', {
        'books': books,
        'series': series,
        'movies': movies,
        'mangas': mangas,
        'num_books': num_books,
        'num_series': num_series,
        'num_movies': num_movies,
        'num_mangas': num_mangas,
        'all_genres': all_genres,
        'items': all_items
    })

@login_required
def home(request):
    books = Book.objects.filter(user=request.user)
    series = Series.objects.filter(user=request.user)
    movies = Movie.objects.filter(user=request.user)
    mangas = Manga.objects.filter(user=request.user)
    return render(request, 'media/home.html',
                  {'books': books, 'series': series,
                   'movies': movies, 'manga': mangas})

MODEL_MAP = {
    'book': (Book, BookForm),
    'movie': (Movie, MovieForm),
    'series': (Series, SeriesForm),
    'manga': (Manga, MangaForm)
}

def item_detail(request, model_name, item_id):
    mapping = MODEL_MAP.get(model_name)
    if not mapping:
        raise Http404("Type inconnu")

    model, form_class = mapping
    instance = get_object_or_404(model, id=item_id, user=request.user)

    form = form_class(instance=instance)  # Génère le formulaire pré-rempli (non modifiable ici)

    return render(request, 'media/detail_item.html', {
        'instance': instance,
        'form': form,
        'model_name': model_name,
    })

@login_required
def add_manga(request):
    if request.method == 'POST':
        form = MangaForm(request.POST, request.FILES)
        if form.is_valid():
            manga = form.save(user=request.user)
            return redirect('profile')
    else:
        form = MangaForm()
    
    # Envoie tous les genres pour peupler la liste Select2
    all_genres = Genre.objects.all()

    return render(request, 'media/add_item.html', {
        'form': form,
        'title': 'Ajouter un livre',
        'all_genres': all_genres
    })

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(user=request.user)
            return redirect('profile')
    else:
        form = BookForm()
    
    # Envoie tous les genres pour peupler la liste Select2
    all_genres = Genre.objects.all()

    return render(request, 'media/add_item.html', {
        'form': form,
        'title': 'Ajouter un livre',
        'all_genres': all_genres
    })

@login_required
def add_series(request):
    if request.method == 'POST':
        form = SeriesForm(request.POST, request.FILES)
        if form.is_valid():
            # Passer l'utilisateur connecté à la méthode save
            form.save(user=request.user)
            return redirect('profile') 
    else:
        form = SeriesForm()

    # Envoie tous les genres pour peupler la liste Select2
    all_genres = Genre.objects.all()
    return render(request, 'media/add_item.html', {
        'form': form,
        'title': 'Ajouter une série',
        'all_genres': all_genres
    })

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            # Passer l'utilisateur connecté à la méthode save
            form.save(user=request.user)
            return redirect('profile') 
    else:
        form = MovieForm()
    # Envoie tous les genres pour peupler la liste Select2
    all_genres = Genre.objects.all()
    return render(request, 'media/add_item.html', {
        'form': form,
        'title': 'Ajouter un film',
        'all_genres': all_genres
    })
