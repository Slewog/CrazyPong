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

    def load(self, screen_rect: pg.Rect, font_data: dict[str, Any], colors: dict[str, pg.Color]):
        font = load_font(font_data['family'], font_data['size'])
        font_title = load_font(font_data['family'], MENU['title_txt_size'])

        self.title_surf = font_title.render(MENU['title_txt'], True, colors['font'])
        self.title_rect = self.title_surf.get_rect(midtop = (screen_rect.width // 2, screen_rect.height // 3 -  MENU['title_pos_offset']))

        self.copyright_surf = font.render(MENU['copyright_txt'], True, colors['font'])
        self.copyright_rect = self.copyright_surf.get_rect(midbottom = (screen_rect.width // 2, screen_rect.height - MENU['copyright_pos_offset']))

        self.pg_logo_surf = load_img("pygame_logo.png", convert_a=True)
        self.pg_logo_rect = self.pg_logo_surf.get_rect()
        self.pg_logo_rect.right = screen_rect.width - 10
        self.pg_logo_rect.bottom = screen_rect.height - 9

        Button.FONT = font
        Button.FONT_COLOR = colors['font']
        Button.CLICK_SOUND = load_sound("button.wav", BUTTON['sound_vol'])

        self.buttons.append(Button(
            {'text': "1 PLAYER", 'action': 'play', 'level': 'oneplayer'}, (screen_rect.width // 2 - MENU['btn_offset_centerx'], screen_rect.height // 2)
        ))

        self.buttons.append(Button(
            {'text': "2 PLAYER", 'action': 'play', 'level': 'twoplayer'}, (screen_rect.width // 2 + MENU['btn_offset_centerx'], screen_rect.height // 2)
        ))

        self.buttons.append(Button(
            {'text': "QUIT", 'action': 'quit', 'level': None}, (screen_rect.width // 2, self.buttons[1].text_rect.bottom + MENU['btn_offset_centery'])
        ))

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
