import pygame

from pygame.sprite import Sprite
from dino_runner.utils.constants import SCREEN_WIDTH


class Obstacle(Sprite):
    def __init__(self, image, type, is_animated: bool=False):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
        self.step_index = 0
        self.is_animated = is_animated
        self.animated_image = self.image

    def update(self, game_speed, obstacles):
        if self.is_animated:
            self.animated_actions()

        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()


    def animated_actions(self):
        if self.step_index >= 20:
            self.step_index = 0

        image = self.image[0] if self.step_index <= 10 else self.image[1]
        self.animated_image = image

        self.step_index += 1


    def draw(self, screen):
        if not self.is_animated:
            return screen.blit(self.image[self.type], (self.rect.x, self.rect.y))

        screen.blit(self.animated_image, (self.rect.x, self.rect.y))