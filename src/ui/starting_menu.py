import pygame as pg
from typing import List

from src.const.custom_typing import FontData
from src.const.settings import STARTING_MENU
from src.utils import load_font, Text, Image
from .components.buttons import ButtonAnimate


class StartingMenu:
    def __init__(self, font_data: FontData) -> None:
        # Setup.
        self.all = pg.sprite.Group()
        
        font = load_font(font_data['family'], font_data['default_size'])

        # Creation of the menu.
        self.buttons = [ButtonAnimate(button[0], button[1]) for button in STARTING_MENU['buttons']]

        title = STARTING_MENU['title']
        Text(
            load_font(font_data['family'], font_data['title_size']),
            title['text'],
            title['pos'],
            title['center_by'],
            self.all,
            bg=True,
            bg_offset_y=-10
        )
        
        copyright = STARTING_MENU['copyright']
        Text(font, copyright['text'], copyright['pos'], copyright['center_by'], self.all, bg=True)

        pg_logo = STARTING_MENU['pg_logo']
        Image(pg_logo['file'], pg_logo['pos'], self.all)
    
    def handle_btn_click(self) -> None:
        for button in self.buttons:
            if button.hovered:
                button.click()
                break

    def render(self, display_surf: pg.Surface) -> None:
        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            button.render(display_surf, mouse_pos)
        
        self.all.draw(display_surf)
