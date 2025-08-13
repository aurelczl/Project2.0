import sys
import pygame
import requests
import random
import argparse 
from PIL import Image
from io import BytesIO

# --- Parsing des arguments (token reçu depuis la page web) ---
parser = argparse.ArgumentParser()
parser.add_argument("--token", required=True, help="Token utilisateur Django")
args = parser.parse_args()
TOKEN = args.token

API_URL = "http://127.0.0.1:8000/api/game/save/"
API_URL_LIST = "http://127.0.0.1:8000/api/game/list/"  # adapte si ton site est en ligne
PLAYER_INFO_URL = "http://127.0.0.1:8000/api/game/player/"
HEADERS = {"Authorization": f"Token {TOKEN}"}

def get_player_info():
    r = requests.get(PLAYER_INFO_URL, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(f"Erreur API : {r.status_code} - {r.text}")

def get_last_score():
    try:
        r = requests.get(API_URL_LIST, headers=HEADERS)
        if r.status_code == 200:
            scores = r.json()
            if scores:
                return scores[0]["value"]  # le dernier score enregistré
        return 0
    except Exception as e:
        print("Erreur récupération score :", e)
        return 0

def send_score(score):
    """Envoie le score final à Django via l'API REST"""
    data = {"value": score}
    try:
        r = requests.post(API_URL, json=data, headers=HEADERS)
        if r.status_code == 201:
            print("Score envoyé :", r.json())
        else:
            print("Erreur API :", r.text)
    except Exception as e:
        print("Impossible d'envoyer le score :", e)

# === MINI JEU ===
# --- Initialisation Pygame ---
pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 36)
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Mini jeu 2D avec personnage")
clock = pygame.time.Clock()

# --- Chargement du player via API ---
player_data = get_player_info()
print("Nom :", player_data["username"])
print("Classe :", player_data["class"])
print("Stats :", player_data["stats"])

# Charger l'image
img_url = player_data["image_url"]
if img_url:
    img_data = requests.get(img_url).content
    pil_image = Image.open(BytesIO(img_data)).convert("RGBA")
    mode = pil_image.mode
    size = pil_image.size
    
    original_width, original_height = pil_image.size
    new_width = 120
    new_height = int((new_width / original_width) * original_height)
    
    data = pil_image.tobytes()
    player_img = pygame.image.fromstring(data, size, mode)
    player_img = pygame.transform.scale(player_img, (new_width, new_height))
else:
    raise FileNotFoundError("Aucune image disponible pour ce joueur")

# Position & vitesse du joueur
player_x = 150
player_y = 200
player_vel_y = 0
is_jumping = False

# Sol
ground_height = 50

score = get_last_score()
print(f"Score précédent chargé : {score}")

# --- Boucle du jeu ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            send_score(score)
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                player_vel_y = -15  # saut vers le haut
                score += random.randint(1, 5)  # incrément du score

    # --- Logique du saut ---
    if is_jumping:
        player_y += player_vel_y
        player_vel_y += 1  # gravité
        if player_y >= 300:
            player_y = 300
            is_jumping = False

    # --- Dessin ---
    screen.fill((135, 206, 235))  # ciel bleu
    pygame.draw.rect(screen, (34, 139, 34), (0, 350, 800, ground_height))  # sol
    screen.blit(player_img, (player_x, player_y))
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (20, 20))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
