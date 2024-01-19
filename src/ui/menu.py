from typing import Any
import pygame as pg

from ..const.settings import MENU
from ..utils import load_font
from .button import Button


class Menu:
    def __init__(self) -> None:
        self.buttons: list[Button] = []

        self.title_surf: pg.Surface
        self.title_rect: pg.Rect
        self.copyright_surf: pg.Surface
        self.copyright_rect: pg.Rect

    def load(self, screen_rect: pg.Rect, font_data: dict[str, Any], colors: dict[str, pg.Color]):
        font = load_font(font_data['family'], font_data['size'])
        font_title = load_font(font_data['family'], MENU['title_txt_size'])

        self.title_surf = font_title.render(MENU['title_txt'], True, colors['font'])
        self.title_rect = self.title_surf.get_rect(midtop = (screen_rect.width // 2, screen_rect.height // 3 - 50))

        self.copyright_surf = font.render(MENU['copyright_txt'], True, colors['font'])
        self.copyright_rect = self.copyright_surf.get_rect(midbottom = (screen_rect.width // 2, screen_rect.height - 20))

        Button.FONT = font
        Button.FONT_COLOR = colors['font']

        self.buttons.append(Button(
            {'text': "1 PLAYER", 'action': 'play', 'level': 'oneplayer'}, (screen_rect.width // 2 - 175, screen_rect.height // 2)
        ))

        self.buttons.append(Button(
            {'text': "2 PLAYER", 'action': 'play', 'level': 'twoplayer'}, (screen_rect.width // 2 + 175, screen_rect.height // 2)
        ))

        self.buttons.append(Button(
            {'text': "QUIT", 'action': 'quit', 'level': None}, (screen_rect.width // 2, self.buttons[1].text_rect.bottom + 75)
        ))

    def check_for_btn_click(self):
        for button in self.buttons:
            if button.hovered:
                button.click()

    def render(self, display_surf: pg.Surface):
        display_surf.blit(self.title_surf, self.title_rect)

        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            button.check_hover(mouse_pos)
            
            button.check_click()
            button.draw(display_surf)

        display_surf.blit(self.copyright_surf, self.copyright_rect)
