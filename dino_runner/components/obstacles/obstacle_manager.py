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

            if index == 1:
                cactus = Cactus(cactus_image_random, 300)
            else:
                cactus = Cactus(cactus_image_random)

            bird_images = BIRD
            bird = Bird(bird_images)

            obstacles = [bird, cactus]
            self.obstacles.append(choice(obstacles))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                game.playing = False
                game.death_count += 1
                break

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []


"""- mostrar uma mensagem de restart (por exemplo "Press any key to restart")

 - mostrar pontuação atingida

 - mostrar o contador de mortes
 

> Resetar a contagem de pontuação e a velocidade, cada vez que o jogo é "restartado"


> Remover a repetição de código pra formatação de texto em "draw_score()" e "show_menu()"

 >> arquivo "dino_runner\components\game.py"

  >>> draw_score() linhas 82 a 86

  >>> show_menu() linhas 102 a 106
 

 - dica: talvez criar um utilitário para formatar textos, 

  função q pudesse ser reutilizada pra editar todos textos, mudando algumas variáveis tipo: 

   - texto a ser exibido 

   - posição do texto"""