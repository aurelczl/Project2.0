import pygame
import requests

from Code.tool import Tool
from Code.keylistener import KeyListener
from PIL import Image
from io import BytesIO

class Entity(pygame.sprite.Sprite):
    def __init__(self, keylistener: KeyListener, PLAYER_INFO_URL, HEADERS):
        super().__init__()

        player_data = self.get_player_info(PLAYER_INFO_URL, HEADERS)

        #print("player info", player_data)
        perso_class = player_data['class']

        # Animation variables
        self.animation_speed = 0.15
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        
        # Use walk spritesheet for animation
        walk_image_url = f'http://127.0.0.1:8000/media/character_classes/action/{perso_class}/Walk.png'
        
        try:
            spritesheet, original_size = self.image_processing(walk_image_url)
            self.spritesheet = spritesheet
            print(f"Walk image loaded: {original_size}")
            
            # Calculate correct frame size based on spritesheet dimensions
            # 1024x128 with multiple frames horizontally, 128px height is character height
            self.num_frames = 8  # 8 frames dans l'animation
            self.frame_width = original_size[0] // self.num_frames  # 1024 / 8 = 128 pixels
            self.frame_height = original_size[1]  # 128 pixels - hauteur complète du personnage
            
            print(f"Frame size: {self.frame_width}x{self.frame_height}")
            print(f"Number of frames: {self.num_frames}")
            
            # Create animation frames
            self.walk_frames = self.get_walk_frames()
            
            # Set default image
            if self.walk_frames:
                self.image = self.walk_frames[0]
            else:
                # Fallback: create a simple colored surface
                self.image = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
                self.image.fill((255, 0, 0, 128))
                self.walk_frames = [self.image]
                
        except Exception as e:
            print("Walk image ERROR:", e)
            # Fallback
            self.image = pygame.Surface((64, 128), pygame.SRCALPHA)
            self.image.fill((0, 255, 0, 128))
            self.walk_frames = [self.image]
            self.frame_width = 64
            self.frame_height = 128
            self.num_frames = 1

        self.keylistener = keylistener
        self.position = [100, 100]
        self.rect: pygame.Rect = pygame.Rect(self.position[0], self.position[1], self.frame_width, self.frame_height)
        self.is_moving = False

    def image_processing(self, img_url):
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
        self.animate()
        self.rect.topleft = self.position

    def check_move(self):
        self.is_moving = False
        
        if self.keylistener.key_pressed(pygame.K_q):
            self.move_left()
            self.is_moving = True
        elif self.keylistener.key_pressed(pygame.K_d):
            self.move_right()
            self.is_moving = True
        elif self.keylistener.key_pressed(pygame.K_z):
            self.move_up()
            self.is_moving = True
        elif self.keylistener.key_pressed(pygame.K_s):
            self.move_down()
            self.is_moving = True

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            
            if self.is_moving and len(self.walk_frames) > 1:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
                self.image = self.walk_frames[self.current_frame]
            elif not self.is_moving:
                self.current_frame = 0
                self.image = self.walk_frames[0]

    def move_left(self):
        self.position[0] -= 2
        # Pour la gauche, on peut flip l'image horizontalement si besoin
        # self.image = pygame.transform.flip(self.walk_frames[self.current_frame], True, False)

    def move_right(self):
        self.position[0] += 2

    def move_up(self):
        self.position[1] -= 2

    def move_down(self):
        self.position[1] += 2

    def get_walk_frames(self):
        walk_frames = []
        
        # Taille souhaitée (plus petite)
        scaled_width = 64   # Au lieu de 128
        scaled_height = 64  # Au lieu de 128

        # Extraire chaque frame de l'animation
        for frame_index in range(self.num_frames):
            x = frame_index * self.frame_width
            y = 0  # Toujours en haut puisque 128px c'est la hauteur totale
            
            # Extraire la frame du spritesheet
            frame = Tool.split_image(self.spritesheet, x, y, self.frame_width, self.frame_height)
            
            if frame:
                # REDUIRE LA TAILLE ICI
                frame = pygame.transform.scale(frame, (scaled_width, scaled_height))
                walk_frames.append(frame)
        print(f"Total frames extracted: {len(walk_frames)}")
        return walk_frames