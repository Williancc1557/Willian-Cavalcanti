from dino_runner.components.obstacles.obstacles import Obstacle
from random import randint, choice

class Bird(Obstacle):
    def __init__(self, image):
        self.type = randint(0, 1)
        super().__init__(image, self.type, True)
        self.step_index = 0
        self.rect.y = choice([270, 300])
