import json
from io import BytesIO
from django.core import serializers
from django.apps import apps

def export_user_data(user):
    """Génère un JSON des items (sans données utilisateur) prêt au téléchargement direct"""
    data = {'items': {}}
    
    models_to_export = ['Manga', 'Book', 'Series', 'Movie']
    
    for model_name in models_to_export:
        model = apps.get_model('media', model_name)
        items = model.objects.filter(user=user)
        
        serialized_items = []
        for item in items:
            item_data = serializers.serialize('python', [item])[0]['fields']
            item_data.pop('user', None)  # Exclut la référence à l'utilisateur
            
            if 'genres' in item_data:
                item_data['genres'] = list(item.genres.values_list('name', flat=True))
            
            serialized_items.append(item_data)
        
        data['items'][model_name.lower()] = serialized_items

    # Retourne un BytesIO pour téléchargement direct (pas de sauvegarde locale)
    json_data = json.dumps(data, indent=2).encode('utf-8')
    return BytesIO(json_data)

def import_user_data(target_user, json_file):
    """Importe les items dans un nouveau compte utilisateur"""
    data = json.load(json_file)
    
    for model_name, items_data in data.get('items', {}).items():
        model = apps.get_model('media', model_name.capitalize())
        
        for item_data in items_data:
            # Gestion des genres
            genres = item_data.pop('genres', [])
            
            # Crée un nouvel item lié au target_user
            new_item = model.objects.create(
                user=target_user,
                **{k: v for k, v in item_data.items() if k != 'id'}
            )
            
            # Ajoute les genres
            if genres:
                genre_objects = []
                for genre_name in genres:
                    genre, _ = Genre.objects.get_or_create(name=genre_name)
                    genre_objects.append(genre)
                new_item.genres.set(genre_objects)
