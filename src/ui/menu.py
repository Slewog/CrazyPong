from typing import Any, Callable
import pygame as pg

from ..const.settings import MENU
from ..utils import load_font
from .button import Button


class Menu:
    def __init__(self, set_game_state: Callable[[str], None]) -> None:
        self.buttons: list[Button] = []

        self.title_surf: pg.Surface
        self.title_rect: pg.Rect
        self.copyright_surf: pg.Surface
        self.copyright_rect: pg.Rect

        self.set_game_state = set_game_state

    def load(self, screen_rect: pg.Rect, font_data: dict[str, Any], colors: dict[str, pg.Color]):
        font = load_font(font_data['family'], font_data['size'])
        font_title = load_font(font_data['family'], 100)

        self.title_surf = font_title.render(MENU['title'], True, colors['font'])
        self.title_rect = self.title_surf.get_rect(midtop = (screen_rect.width // 2, screen_rect.height // 3 - 50))

        self.copyright_surf = font.render(MENU['copyright'], True, colors['font'])
        self.copyright_rect = self.copyright_surf.get_rect(midbottom = (screen_rect.width // 2, screen_rect.height - 20))

        Button.FONT = font
        Button.FONT_COLOR = colors['font']
        Button.BORDER_COLOR = colors['font']
        Button.BACKGROUND_COLOR = colors['background']
        Button.RADIUS = MENU['btn_radius']

        self.buttons.append(Button(
            {'text': "1 PLAYER", 'type': 'play', 'action': 'oneplayer'}, (screen_rect.width // 2 - 175, screen_rect.height // 2)
        ))

        self.buttons.append(Button(
            {'text': "2 PLAYER", 'type': 'play', 'action': 'twoplayer'}, (screen_rect.width // 2 + 175, screen_rect.height // 2)
        ))

        self.buttons.append(Button(
            {'text': "QUIT", 'type': 'quit', 'action': None}, (screen_rect.width // 2, self.buttons[1].text_rect.bottom + 75)
        ))

    def render(self, display_surf: pg.Surface):
        display_surf.blit(self.title_surf, self.title_rect)

        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            button.draw(display_surf)

            if button.is_hovered(mouse_pos):
                if button.is_clicked():

                    if button.type == "play":
                        pass

                    self.set_game_state(button.type)
                    

        display_surf.blit(self.copyright_surf, self.copyright_rect)
