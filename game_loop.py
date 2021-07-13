import pygame
import os
import random

from pygame.sprite import Sprite, spritecollideany
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.sprite import Group

WIDTH = 1000
HEIGHT = 400
WORLD_WIDTH = 10 * WIDTH
# ROAD = pygame.transform.scale(pygame.image.load(os.path.join("images", "road.jpeg")), (WIDTH, HEIGHT))
ROAD_BORDER_1 = pygame.Rect(0, 77, WIDTH, 10)
ROAD_BORDER_2 = pygame.Rect(0, 310, WIDTH, 10)


class Player(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load("images/start_car.jpeg"), (80, 40))
        self.world_rect = self.image.get_rect().move(0, 200)

    def update(self, keys):
        if keys[pygame.K_SPACE]:  # gas for the car
            self.press_gas_pedal()
        if keys[pygame.K_UP] and self.world_rect.top - 5 > ROAD_BORDER_1.y:
            self.move_up()
        if keys[pygame.K_DOWN] and self.world_rect.bottom < ROAD_BORDER_2.y:
            self.move_down()
        if self.world_rect.left > WORLD_WIDTH:
            self.world_rect.left -= WORLD_WIDTH

    def move_up(self):
        self.world_rect.top -= 10

    def move_down(self):
        self.world_rect.top += 10

    def press_gas_pedal(self):
        self.world_rect.left += 9


class CarWreck(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load("images/xplosion.png"), (90, 50))
        self.world_rect = self.image.get_rect().move(x, y)

    def update(self, *args, **kwargs):
        pass


class EnemiesEasy(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.world_rect = Rect(x, y, 25, 25)
        self.image = pygame.transform.scale(pygame.image.load("images/enemy_car1.png"), (80, 40))

    def update(self):
        self.world_rect.move_ip(-3, 0)


class EnemiesMedium(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.world_rect = Rect(x, y, 25, 25)
        self.image = pygame.transform.scale(pygame.image.load("images/enemy_car2.jpeg"), (80, 40))

    def update(self):
        self.world_rect.move_ip(-5, 0)


class EnemiesHard(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.world_rect = Rect(x, y, 25, 25)
        self.image = pygame.transform.scale(pygame.image.load("images/enemy_car3 copy.jpg"), (80, 40))

    def update(self):
        self.world_rect.move_ip(-7, 0)


class RaceTrack(Sprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.transform.scale(pygame.image.load("images/road.jpeg"), (WORLD_WIDTH, HEIGHT))
        self.world_rect = self.image.get_rect()
        self.world_rect.bottom = HEIGHT
        # assert self.world_rect.width == WORLD_WIDTH


class Viewport:
    def __init__(self):
        self.left = 0

    def update(self, sprite):
        self.left = sprite.world_rect.left - 300
        if self.left > WORLD_WIDTH:
            self.left -= WORLD_WIDTH
        if self.left < 0:
            self.left += WORLD_WIDTH

    def remake_rect(self, group, dx=0):
        for sprite in group:
            sprite.rect = sprite.world_rect.move(-self.left + dx, 0)

    def draw(self, group, surface):
        self.remake_rect(group)
        group.draw(surface)
        self.remake_rect(group, WORLD_WIDTH)
        group.draw(surface)


class GameLoop:
    def __init__(self):
        pygame.display.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("My Car Racing Game")
        self.player = Player()
        self.player_group = Group()
        self.player_group.add(self.player)
        self.enemies = Group()
        # You may have to change these if you want any chance at beating this game
        for i in range(18):
            self.enemies.add(EnemiesEasy(random.randrange(1000, WORLD_WIDTH - 300), random.randrange(80, 275)))
        for i in range(12):
            self.enemies.add(EnemiesMedium(random.randrange(5500, WORLD_WIDTH - 300), random.randrange(80, 275)))
        for i in range(5):
            self.enemies.add(EnemiesHard(random.randrange(9000, WORLD_WIDTH - 300), random.randrange(80, 275)))
        self.static_sprites = Group()
        self.static_sprites.add(RaceTrack())
        self.viewport = Viewport()
        self.viewport.update(self.player)

    def game_loop(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            self.draw()
            self.update()
            pygame.display.flip()
            clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
                if event.key == pygame.K_UP:
                    pass
                if event.key == pygame.K_DOWN:
                    pass

    def update(self):
        self.player_group.update(pygame.key.get_pressed())
        self.enemies.update()
        if self.player.alive and (collision_culprit := spritecollideany(self.player, self.enemies)):
            self.player.kill()
            collision_culprit.kill()
            self.player_group.add(CarWreck(self.player.world_rect.left, self.player.world_rect.top))
        self.viewport.update(self.player)

    def draw(self):
        self.viewport.draw(self.static_sprites, self.screen)
        self.viewport.draw(self.player_group, self.screen)
        self.viewport.draw(self.enemies, self.screen)
        pygame.draw.rect(self.screen, (0, 0, 0), ROAD_BORDER_1)
        pygame.draw.rect(self.screen, (0, 0, 0), ROAD_BORDER_2)


if __name__ == '__main__':
    game = GameLoop()
    game.game_loop()
