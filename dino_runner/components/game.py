from sre_constants import JUMP
from tracemalloc import start
import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.utils.constants import BG, CLOUD, COLORS, FONT_STYLE, GAME_OVER, ICON, JUMPING, LIFE, RESET, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.text_utils import show_text
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.y_pos_cloud = 120
        self.score = 0
        self.death_count = 0
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.best_score = 0
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.playing = True
        self.reset_score()
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.game_speed = 20
        self.score = 0
        self.player.dino_life = 3

        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.obstacle_manager.update(self)
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.update_score()
        self.power_up_manager.update(self.score, self.game_speed, self.player)


    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 3

        self.draw_score()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill(COLORS["WHITE"]) #Também aceita código hexadecimal "#FFFFFF"
        self.draw_background()
        self.obstacle_manager.draw(self.screen)
        self.player.draw(self.screen)
        self.draw_power_up_time()
        self.draw_score()
        self.draw_life()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(CLOUD, (self.x_pos_bg, self.y_pos_cloud))
        self.screen.blit(CLOUD, (image_width + self.x_pos_bg, self.y_pos_cloud))

        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        show_text(f"Score: {self.score}", (1000, 50), COLORS["BLACK"], screen=self.screen)

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                show_text(f"{self.player.type.capitalize()} enabled for {time_to_show} seconds.", screen=self.screen,
                                        font_size = 18,
                                        position=(500, 40),
                                        color=COLORS["BLACK"])
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def show_menu(self):
        self.screen.fill(COLORS["WHITE"])


        if self.death_count == 0:
            self.start_menu()
        else:
            self.lost_menu()

        pygame.display.update()
        self.handle_events_on_menu()

    def start_menu(self):
        half_screen_width = SCREEN_WIDTH // 2
        half_screen_height = SCREEN_HEIGHT // 2

        self.screen.blit(JUMPING, self.centralize(JUMPING, half_screen_width, half_screen_height - 120))
        show_text("Press any key to start", (half_screen_width, half_screen_height), COLORS["BLACK"], screen=self.screen)

    def lost_menu(self):
        half_screen_width = SCREEN_WIDTH // 2
        half_screen_height = SCREEN_HEIGHT // 2

        show_text(f"Your deaths: {self.death_count}", (20, 20), COLORS["BLACK"], is_center=False, screen=self.screen)

        self.screen.blit(ICON, self.centralize(ICON, half_screen_width, half_screen_height - 120))
        self.screen.blit(GAME_OVER, self.centralize(GAME_OVER, half_screen_width, half_screen_height - 220))

        show_text(f"Your score: {self.score}", (half_screen_width, half_screen_height), COLORS["BLACK"], 25, screen=self.screen)
        show_text(f"Your best score: {self.best_score}", (half_screen_width, half_screen_height + 40), COLORS["BLACK"], screen=self.screen)
        show_text("Press any key to restart", (half_screen_width, half_screen_height + 160), COLORS["BLACK"], 22, screen=self.screen)
        self.screen.blit(RESET, self.centralize(RESET, half_screen_width, half_screen_height + 240))

    def reset_score(self):
        self.game_speed = 20
        self.score = 0

    def centralize(self, image, width, height):
        image_rect = image.get_rect()
        image_rect.center = (width, height)
        return image_rect

    def draw_life(self):
        self.screen.blit(LIFE, (10, 10))
        show_text(
            str(self.player.dino_life),
            position=(50, 10),
            color=COLORS["BLACK"],
            is_center=False,
            screen=self.screen
        )
