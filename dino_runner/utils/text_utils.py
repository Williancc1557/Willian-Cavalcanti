import pygame

from dino_runner.utils.constants import FONT_STYLE

def show_text(value: str, position: tuple, color: tuple or str, font_size=22, is_center=True, screen=None):
    font = pygame.font.Font(FONT_STYLE, font_size)
    text = font.render(value, True, color)
    text_rect = text.get_rect()

    text_rect.center = position

    position_selected = text_rect if is_center else position

    screen.blit(text, position_selected)