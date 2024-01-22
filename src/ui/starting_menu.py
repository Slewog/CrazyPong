import pygame as pg
from typing import List

from src.const.custom_typing import FontData
from src.const.settings import STARTING_MENU
from src.utils import load_font, Text, Image
from .components.buttons import ButtonAnimate


class StartingMenu:
    def __init__(self, font_data: FontData) -> None:
        # Setup.
        self.buttons: List[ButtonAnimate] = []

        self.all_text = pg.sprite.Group()
        self.all_img = pg.sprite.Group()
        
        font = load_font(font_data['family'], font_data['default_size'])

        # Creation of the menu.
        for button in STARTING_MENU['buttons']:
            self.buttons.append(ButtonAnimate(button[0], button[1]))

        title = STARTING_MENU['title']
        Text(
            load_font(font_data['family'], font_data['title_size']),
            title['text'],
            title['pos'],
            title['center_by'],
            self.all_text,
            bg=True,
            bg_offset_y=-10
        )
        

        copyright = STARTING_MENU['copyright']
        Text(font, copyright['text'], copyright['pos'], copyright['center_by'], self.all_text, bg=True)


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
        
        self.all_text.draw(display_surf)
        self.all_img.draw(display_surf)
