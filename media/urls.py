from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/book/', views.add_book, name='add_book'),
    path('add/series/', views.add_series, name='add_series'),
    path('add/movie/', views.add_movie, name='add_movie'),
    path('add/manga/', views.add_manga, name='add_manga'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),


    # Détails de chaque élément
    #path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    #path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    #path('series/<int:series_id>/', views.series_detail, name='series_detail'),

    path('<str:model_name>/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('<str:model_name>/<int:item_id>/', views.item_detail, name='item_detail'),
    path('<str:model_name>/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    
    path('search/', views.search, name='search'),
    path('genre/add/', views.add_genre, name='add_genre'),
    path('library/', views.library_view, name='library'),
    path('admin/load_data/', views.load_data, name='load_data'),

    # Pour openlibrary : Ancienne version
    #path('api/fetch-book-info-openlib/', views.fetch_book_info_openlib, name='fetch_book_info_openlib'),
    #path('api/book-suggestions-openlib/', views.book_suggestions_openlib, name='book_suggestions_openlib'),
    # Pour choix openlib/babelio/booknode :
    path('api/book-suggestions/', views.book_suggestions, name='book_suggestions'),
    path('api/fetch-book-info/', views.fetch_book_info, name='fetch_book_info'),



]

