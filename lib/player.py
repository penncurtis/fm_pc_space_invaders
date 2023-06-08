import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load('./lib/assets/player.png')
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.shoot_time = 0
        self.shoot_cooldown = 600

        self.bullets = pygame.sprite.Group()

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot()
            self.ready = False
            self.shoot_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.shoot_cooldown:
                self.ready = True

    def shoot(self):
        self.bullets.add(Bullet(self.rect.center, -8, self.rect.bottom))

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.bullets.update()