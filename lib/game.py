import pygame, sys
import sqlite3
from random import choice
from player import Player
from alien import Alien
from bullet import Bullet


class Game:

    def __init__(self):
        self.player_name = " "
        player_sprite = Player((screen_width / 2, screen_height), screen_width, 5 )
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.start_game = False
        self.game_over = False

        self.lives = 3
        self.live_surf = pygame.image.load("./lib/assets/icon_1.png").convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font("./lib/assets/space_invaders.ttf", 20)

        self.aliens = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 1

    def alien_setup(self, rows, cols, x_distance = 60, y_distance = 48, x_offset = 70, y_offset = 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                alien_sprite = Alien(x, y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        if not self.aliens:
            self.alien_setup(rows=6, cols=8)
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            bullet_sprite = Bullet(random_alien.rect.center, 6, screen_height)
            self.alien_bullets.add(bullet_sprite)

    def collision_checks(self):

        if self.player.sprite.bullets:
            for bullet in self.player.sprite.bullets:
                aliens_hit = pygame.sprite.spritecollide(bullet, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    bullet.kill()
        
        if self.alien_bullets:
            for bullet in self.alien_bullets:
                if pygame.sprite.spritecollide(bullet, self.player, False):
                    bullet.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True

        if self.aliens:
            for alien in self.aliens:
                if pygame.sprite.spritecollide(alien, self.player, False):
                    self.game_over = True

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft = (0, 0))
        screen.blit(score_surf, score_rect)

    def end_message(self):
        loss_surf = self.font.render("GAME OVER", False, "white")
        loss_rect = loss_surf.get_rect(center = (screen_width / 2, screen_height / 2))
        screen.blit(loss_surf, loss_rect)
    
    def start_menu(self):
        start_surf = self.font.render("START GAME? (press space)", False, "white")
        start_rect = start_surf.get_rect(center = (screen_width / 2, screen_height / 2))
        screen.blit(start_surf, start_rect)
        
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.start_game = True
            self.player_name = input("Enter Name:")

    def save_score_to_database(self):
        conn = sqlite3.connect("game_scores.db")
        c = conn.cursor()

        c.execute("CREATE TABLE IF NOT EXISTS scores (player_name text, score integer)")
        c.execute("SELECT * FROM scores WHERE player_name = ?", (self.player_name,))
        existing_entry = c.fetchone()

        if existing_entry:
            if self.score > existing_entry[1]:
                c.execute("UPDATE scores SET score = ? WHERE player_name = ?", (self.score, self.player_name))
        else:
            c.execute("INSERT INTO scores (player_name, score) VALUES (?, ?)", (self.player_name, self.score))

        conn.commit()
        conn.close()

    def run(self):
        if not self.start_game:
            self.start_menu()
            self.get_input()

        if self.start_game and not self.game_over:
            self.player.update()
            self.aliens.update(self.alien_direction)
            self.alien_bullets.update()

            self.alien_position_checker()
            self.collision_checks()

            self.player.sprite.bullets.draw(screen)
            self.player.draw(screen)
            self.aliens.draw(screen)
            self.alien_bullets.draw(screen)
            self.display_lives()
            self.display_score()

        if self.game_over:
            self.end_message()
            self.save_score_to_database()

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()

    ALIENBULLET = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENBULLET, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENBULLET:
                game.alien_shoot()
        
        screen.fill((30,30,30))

        game.run()

        pygame.display.flip()
        clock.tick(60)