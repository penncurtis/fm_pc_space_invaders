import pygame

class Alien(pygame.sprite.Sprite):

    def __init__(self, file, x, y):
        super().__init__()
        file_path = f"./lib/assets/{file}.png"
        self.image = pygame.image.load(file_path)
        self.rect = self.image.get_rect(topleft = (x,y))
        if file == 'basic_alien':
            self.value = 10
        elif file == 'upgraded_alien':
            self.value = 20
        elif file == 'best_alien':
            self.value = 50

    def update(self, direction):
        self.rect.x += direction