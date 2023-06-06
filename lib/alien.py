import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('./lib/assets/icon_2.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))
        self.value = 100

    def update(self, direction):
        self.rect.x += direction