from django.test import TestCase

# Create your tests here.

######## IMPORT SELECTED ITEMS :: TESTS ######

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import PublicBook, Book, PublicManga, Manga, Genre

import json

class ImportSelectedItemsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.url = reverse('import_selected_items')  # Assure-toi d’avoir nommé ta vue
        self.client.login(username='testuser', password='testpass')

    def test_import_valid_book(self):
        data = {
            "book": [
                {
                    "title": "1984",
                    "statut": "Lu",
                    "finished_year": 2024,
                    "finished_month": 8,
                    "finished_day": 1,
                    "global_rate": 95,
                    "genres": ["Science-Fiction", "Dystopie"],
                    "author": "George Orwell",
                    "edition": "Folio",
                    "pageCount": 328
                }
            ]
        }

        response = self.client.post(
            self.url,
            json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 1)
        book = Book.objects.first()
        self.assertEqual(book.public_book.title, "1984")
        self.assertEqual(book.user, self.user)
        self.assertEqual(book.global_rate, 95)
        self.assertEqual(book.genres.count(), 2)

    def test_import_missing_title(self):
        data = {
            "book": [
                {
                    "statut": "Lu"
                }
            ]
        }
        response = self.client.post(
            self.url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("titre manquant", response.json()["message"])

    def test_invalid_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
    
    def test_import_valid_manga_with_title(self):
        data = {
            "manga": [
                {
                    "title": "Chainsaw Man",
                    "statut": "Fini",
                    "scan": "MangaPlus",
                    "reading_website": "https://mangasite.com/chainsaw-man",
                    "finished_year": 2025,
                    "finished_month": 7,
                    "finished_day": 10,
                    "global_rate": 92,
                    "genres": ["Action", "Horreur", "Fantastique"]
                }
            ]
        }

        response = self.client.post(
            self.url,
            json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Manga.objects.count(), 1)

        manga = Manga.objects.first()
        self.assertEqual(manga.public_manga.title, "Chainsaw Man")
        self.assertEqual(manga.user, self.user)
        self.assertEqual(manga.statut, "Fini")
        self.assertEqual(manga.scan, "MangaPlus")
        self.assertEqual(manga.genres.count(), 3)
        
    def test_import_valid_manga_with_id(self):
        public = PublicManga.objects.create(title="One Piece")
        data = {
            "manga": [
                {
                    "public_manga": public.id,
                    "statut": "En cours",
                    "scan": None,
                    "reading_website": None,
                    "finished_year": 2025,
                    "finished_month": 8,
                    "finished_day": 1,
                    "global_rate": 80,
                    "genres": ["Aventure"]
                }
            ]
        }

        response = self.client.post(
            self.url,
            json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Manga.objects.count(), 1)

        manga = Manga.objects.first()
        self.assertEqual(manga.public_manga, public)
        self.assertEqual(manga.statut, "En cours")
        self.assertEqual(manga.genres.count(), 1)
