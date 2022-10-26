import pygame
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD
from random import randint, choice

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            cactus_images = [SMALL_CACTUS, LARGE_CACTUS]
            index = randint(0, 1)
            cactus_image_random = cactus_images[index]
            cactus = Cactus(cactus_image_random)

            if index == 1:
                cactus = Cactus(cactus_image_random, 300)

            bird_images = BIRD
            bird = Bird(bird_images)

            obstacles = [bird, cactus]
            self.obstacles.append(choice(obstacles))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                game.playing = False
                break

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)