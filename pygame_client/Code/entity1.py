import pygame
import requests

from Code.tool import Tool
from Code.keylistener import KeyListener
from PIL import Image
from io import BytesIO

class Entity(pygame.sprite.Sprite): #Fait pour un spritesheet
    def __init__(self, keylistener: KeyListener, PLAYER_INFO_URL, HEADERS):
        super().__init__()

        player_data = self.get_player_info(PLAYER_INFO_URL, HEADERS)

        print("player info", player_data)
        img_url = player_data["image_url"]
        perso_class = player_data["class"]
        if perso_class == "Mage":
            perso_class = 'Enchantress'
            
            walk_image_url = 'http://127.0.0.1:8000/media/character_classes/male/Walk.png'
        
        player_size = [32, 48]
        if img_url:
            spritesheet, size = self.image_processing(img_url, player_size)
            # Sauvegarder le spritesheet complet
            self.spritesheet = spritesheet  
            
            # Découper un sprite dedans
            self.image = Tool.split_image(self.spritesheet, 0, 0, size[0], size[1])
            self.image = pygame.transform.scale(self.image, (player_size[0], player_size[1]))
            
            if walk_image_url :
                try : 
                    spritesheet, _ = self.image_processing(walk_image_url, player_size)
                    # Sauvegarder le spritesheet complet
                    self.spritesheet = spritesheet 
                    print("walk image devient spritesheet")
                except Exception as e :
                    print("Walk image ERROR :", e)
        else:
            raise FileNotFoundError("Aucune image disponible pour ce joueur")

        self.keylistener = keylistener
        self.position = [0, 0]
        self.rect: pygame.Rect = pygame.Rect(0, 0, player_size[0], player_size[1])
        self.all_images = self.get_all_images(player_size)
        self.index_image = 0

    def image_processing(self, img_url, player_size):
        # Télécharger et convertir l'image
        img_data = requests.get(img_url).content
        pil_image = Image.open(BytesIO(img_data)).convert("RGBA")
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()
        spritesheet = pygame.image.fromstring(data, size, mode).convert_alpha()
        return spritesheet, size

    def get_player_info(self, PLAYER_INFO_URL, HEADERS):
        r = requests.get(PLAYER_INFO_URL, headers=HEADERS)
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception(f"Erreur API : {r.status_code} - {r.text}")

    def update(self):
        self.check_move()
        self.rect.topleft = self.position


    def check_move(self):
        if self.keylistener.key_pressed(pygame.K_q):
            self.move_left()
        elif self.keylistener.key_pressed(pygame.K_d):
            self.move_right()
        elif self.keylistener.key_pressed(pygame.K_z):
            self.move_up()
        elif self.keylistener.key_pressed(pygame.K_s):
            self.move_down()

# Diffrent move depending on the tuileset of the caracters : 16x16 6 cases for une frame 
# move rigth is the walking original frames, going left is the symetric 

    def move_left(self):
        self.position[0] -= 1
        self.image = self.all_images["left"][self.index_image]

    def move_right(self):
        self.position[0] += 1
        self.image = self.all_images["right"][self.index_image]

    def move_up(self):
        self.position[1] -= 1
        self.image = self.all_images["up"][self.index_image]

    def move_down(self):
        self.position[1] += 1
        self.image = self.all_images["down"][self.index_image]

    def get_all_images(self, player_size):
        all_images = {
            "down": [],
            "left": [],
            "right": [],
            "up": []
        }
        for i in range(8):
            for j, key in enumerate(all_images.keys()):
                all_images[key].append(Tool.split_image(self.spritesheet, i*16, j*16, 16, 16))
        return all_images
