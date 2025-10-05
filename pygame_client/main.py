import sys
import pygame
import requests
import random
import argparse 

from Code.maps import *
from Code.game import Game

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


pygame.init()

if __name__ == "__main__":
    game = Game(PLAYER_INFO_URL, HEADERS)
    game.run()