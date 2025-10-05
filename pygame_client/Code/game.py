import pygame

from Code.screen import Screen
from Code.maps import Map
from Code.keylistener import KeyListener

from Code.entity import Entity

class Game:
    def __init__(self, PLAYER_INFO_URL, HEADERS):
        self.running = True
        self.screen = Screen()
        self.map = Map(self.screen)
        self.keylistener = KeyListener()
        self.entity = Entity(self.keylistener, PLAYER_INFO_URL, HEADERS)
        self.map.add_player(self.entity)

    def run(self):
        while self.running:
            self.handle_input()
            self.map.update()
            self.screen.update()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                self.keylistener.add_key(event.key)
            elif event.type == pygame.KEYUP:
                self.keylistener.remove_key(event.key)