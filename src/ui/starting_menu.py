from typing import Any
import pygame as pg

from ..const.settings import STARTING_MENU, BUTTON
from ..utils import load_font, load_sound

from .sprites_components import Text, TextBackground, Image
from .buttons import AnimateButton as Button


class StartingMenu:
    title_surf: pg.Surface
    title_rect: pg.Rect
    title_bg_rect: pg.Rect
    copyright_surf: pg.Surface
    copyright_rect: pg.Rect
    copyright_bg_rect: pg.Rect

    pg_logo_surf: pg.Surface
    pg_logo_rect: pg.Rect

    def __init__(self, font_data: dict[str, Any], font_color: pg.Color, bg_color: pg.Color) -> None:
        self.buttons: list[Button] = []

        self.all_text = pg.sprite.Group()
        self.all_bg = pg.sprite.Group()
        self.all_img = pg.sprite.Group()
        
        self.font = load_font(font_data['family'], font_data['size'])
        self.font_data = font_data
        self.font_color = font_color
        self.bg_color = bg_color

        Text.COLOR = font_color
        TextBackground.COLOR = bg_color

        Button.FONT = self.font
        Button.FONT_COLOR = font_color
        Button.CLICK_SOUND = load_sound(BUTTON['sound_file'], BUTTON['sound_vol'])

        self.create_menu()

    def create_menu(self):
        for button in STARTING_MENU['buttons']:
            self.buttons.append(Button(button[0], button[1]))
        
        title = STARTING_MENU['title']
        self.title = Text(
            load_font(self.font_data['family'], title['font_size']),
            title['text'],
            title['pos'],
            'midtop',
            self.all_text
        )
        TextBackground(self.title.rect, self.all_bg, offset_y=-10)

        copyright = STARTING_MENU['copyright']
        self.copyright = Text(self.font, copyright['text'], copyright['pos'], 'midbottom', self.all_text)
        TextBackground(self.copyright.rect, self.all_bg)

        pg_logo = STARTING_MENU['pg_logo']
        Image(pg_logo['file'], pg_logo['pos'], self.all_img)

    def handle_btn_click(self):
        for button in self.buttons:
            if button.hovered:
                button.click()

    def render(self, display_surf: pg.Surface):
        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            button.check_hover(mouse_pos)
            button.check_click()
            button.draw(display_surf)
        
        self.all_bg.draw(display_surf)
        self.all_text.draw(display_surf)
        self.all_img.draw(display_surf)
