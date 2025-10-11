from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ScoreSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token

from .models import Score, Player, CharacterClass
from .forms import PlayerCreationForm
from django.views.decorators.csrf import csrf_exempt

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.views.decorators.http import require_GET

###################### BASE DE GESTION DU JEU #############################

@require_GET
def launch_game(request):
    return JsonResponse({
        'status': 'success',
        'message': 'Endpoint de lancement fonctionnel',
        'command': 'python game/main.py --token YOUR_TOKEN'
    })

@login_required
def create_player(request):
    """Création unique d'un joueur"""
    if Player.objects.filter(user=request.user).exists():
        return redirect("game/play.html")

    classes = CharacterClass.objects.all()

    attributes_keys = [
        "description", "intelligence", "agility", "strength",
        "magic", "charism", "wisdom", "constitution"
    ]

    # Prépare une structure JSON avec les infos utiles pour chaque classe
    classes_data = {}
    for c in classes:
        classes_data[c.id] = {
            "name": c.name,
            "attributes": {key: getattr(c, key) for key in attributes_keys},
            "image_male": c.default_image_male.url if c.default_image_male else "",
            "image_female": c.default_image_female.url if c.default_image_female else "",
        }

    if request.method == "POST":
        char_class_id = request.POST.get("character_class")
        try:
            char_class = CharacterClass.objects.get(id=char_class_id)
        except CharacterClass.DoesNotExist:
            return render(request, "game/create_player.html", {
                "classes": classes,
                "error": "Classe invalide"
            })

        image = request.FILES.get("image")

        player = Player(
            user=request.user,
            character_class=char_class,
            intelligence=char_class.intelligence,
            agility=char_class.agility,
            strength=char_class.strength,
            magic=char_class.magic,
            charism=char_class.charism,  # corrige social → charism
            wisdom=char_class.wisdom,
            constitution=char_class.constitution
        )

        if image:
            player.image = image
        else:
            choice = request.POST.get("default_image_choice")
            if choice == "M":
                player.image = char_class.default_image_male
            elif choice == "F":
                player.image = char_class.default_image_female

        player.save()
        return redirect('play_view')

    return render(request, "game/create_player.html", {
        "classes": classes,
        "classes_json": json.dumps(classes_data, cls=DjangoJSONEncoder),
    })
    
@login_required
def play_view(request):
    
    try:
        player = Player.objects.get(user=request.user)
    except Player.DoesNotExist:
        player = None

    token, _ = Token.objects.get_or_create(user=request.user)

    return render(request, "game/play.html", {
        "player": player,
        "token": token.key
    })

@login_required
def player_profile(request):
    """ Affiche le profil du joueur """
    player = get_object_or_404(Player, user=request.user)
    return render(request, "game/player_profile.html", {"player": player})

@login_required
def delete_player(request):
    """ Supprime le joueur après confirmation """
    player = get_object_or_404(Player, user=request.user)
    if request.method == "POST":
        player.delete()
        return redirect("create_player")  # redirection vers création
    return render(request, "game/confirm_delete.html", {"player": player})

##################### Lien API Django et jeu pygame ######################

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_score(request):
    serializer = ScoreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_scores(request):
    scores = Score.objects.filter(user=request.user).order_by('-created_at')
    serializer = ScoreSerializer(scores, many=True)
    return Response(serializer.data)

#API informations joueurs
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def player_info(request):
    try:
        player = get_object_or_404(Player, user=request.user)  # OneToOne relation via user
    except Player.DoesNotExist:
        return Response({"error": "Aucun joueur trouvé"}, status=404)

    # Récupération de l'image avec ta méthode existante
    image_url = player.displayed_image
    if image_url:
        image_url = request.build_absolute_uri(image_url)  # URL absolue

    return Response({
        "username": player.user.username,
        "class": player.character_class.name if player.character_class else None,
        "image_url": image_url,
        "stats": player.performances  # <-- toutes les stats ici
    })