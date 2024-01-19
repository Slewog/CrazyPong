from typing import Any
import pygame as pg

from ..const.settings import MENU, BUTTON
from ..utils import load_font, load_sound, load_img
from .button import Button


class Menu:
    title_surf: pg.Surface
    title_rect: pg.Rect
    copyright_surf: pg.Surface
    copyright_rect: pg.Rect

    pg_logo_surf: pg.Surface
    pg_logo_rect: pg.Rect

    def __init__(self) -> None:
        self.buttons: list[Button] = []

    def load(self, screen_rect: pg.Rect, font_data: dict[str, Any], font_color: pg.Color):
        font = load_font(font_data['family'], font_data['size'])

        title = MENU['title']
        font_title = load_font(font_data['family'], title['font_size'])
        self.title_surf = font_title.render(title['text'], True, font_color)
        self.title_rect = self.title_surf.get_rect(midtop = title['pos'])

        copyright = MENU['copyright']
        self.copyright_surf = font.render(copyright['text'], True, font_color)
        self.copyright_rect = self.copyright_surf.get_rect(midbottom = copyright['pos'])

        pg_logo = MENU['pg_logo']
        self.pg_logo_surf = load_img(pg_logo['file'], convert_a=True)
        self.pg_logo_rect = self.pg_logo_surf.get_rect(bottomright = pg_logo['pos'])

        Button.FONT = font
        Button.FONT_COLOR = font_color
        Button.CLICK_SOUND = load_sound("button.wav", BUTTON['sound_vol'])

        for button in MENU['buttons']:
            print(button)
            self.buttons.append(Button(button[0], button[1]))

    def handle_btn_click(self):
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

        display_surf.blit(self.pg_logo_surf, self.pg_logo_rect)
