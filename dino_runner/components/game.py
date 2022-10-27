import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.utils.constants import BG, COLORS, FONT_STYLE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager

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
        self.score = 0
        self.death_count = 0
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.best_score = 0

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.reset_score()
        self.obstacle_manager.reset_obstacles()
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

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 3

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill(COLORS["WHITE"]) #Também aceita código hexadecimal "#FFFFFF"
        self.draw_background()
        self.obstacle_manager.draw(self.screen)
        self.player.draw(self.screen)
        self.draw_score()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        self.show_text(f"Score: {self.score}", (1000, 50), COLORS["BLACK"])

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):
        self.screen.fill(COLORS["WHITE"])
        half_screen_width = SCREEN_WIDTH // 2
        half_screen_height = SCREEN_HEIGHT // 2

        if self.death_count == 0:
            self.show_text("Press any key to start", (half_screen_width, half_screen_height), COLORS["BLACK"])
        else:
            self.lost_menu()

        pygame.display.update()
        self.handle_events_on_menu()


    def lost_menu(self):
        half_screen_width = SCREEN_WIDTH // 2
        half_screen_height = SCREEN_HEIGHT // 2

        self.show_text(f"Your best score: {self.best_score}", (20, 20), COLORS["BLACK"], is_center=False)
        self.show_text(f"Your deaths: {self.death_count}", (20, 60), COLORS["BLACK"], is_center=False)

        icon_rect = ICON.get_rect()
        icon_rect.center = (half_screen_width, half_screen_height - 120)
        self.screen.blit(ICON, icon_rect)

        self.show_text("You Lost", (half_screen_width, half_screen_height - 220), COLORS["RED"], 30)
        self.show_text(f"Your score: {self.score}", (half_screen_width, half_screen_height), COLORS["BLACK"], 25)
        self.show_text("Press any key to restart", (half_screen_width, half_screen_height + 140), COLORS["BLACK"], 22)


    def show_text(self, value: str, position: tuple, color: tuple or str, font_size=22, is_center=True):
        font = pygame.font.Font(FONT_STYLE, font_size)
        text = font.render(value, True, color)
        text_rect = text.get_rect()

        text_rect.center = position

        position_selected = text_rect if is_center else position

        self.screen.blit(text, position_selected)

    def reset_score(self):
        self.game_speed = 20
        self.score = 0

