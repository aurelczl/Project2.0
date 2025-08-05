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
    
    # Pages Publiques
    path('public_dynamic_page/', views.public_dynamic_page, name='public_content'),
    path('content/<str:content_type>/<int:content_id>/', views.public_content_info, name='public_content_info'),

    path('<str:model_name>/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('<str:model_name>/<int:item_id>/', views.item_detail, name='item_detail'),
    path('<str:model_name>/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    
    path('search/', views.search, name='search'),
    path('genre/add/', views.add_genre, name='add_genre'),
    path('library/', views.library_view, name='library'),
    
    # Pour choix openlib/babelio/booknode :
    path('api/book-suggestions/', views.book_suggestions, name='book_suggestions'),
    path('api/fetch-book-info/', views.fetch_book_info, name='fetch_book_info'),
    
    path('api/search-books/', views.search_books, name='search_books'),
    path('api/search-mangas/', views.search_mangas, name='search_mangas'),

    path('backup/', views.backup_account, name='backup'),
    path('import-selected/', views.import_selected_items, name='import_selected_items'),


]

