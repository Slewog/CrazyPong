from typing import List
from pygame import Surface, mouse

from src.const.custom_typing import FontsDict
from src.const.settings import STARTING_MENU
from src.utils import Text
from .button import ButtonAnimate

class StartingMenu:
    def __init__(self, fonts: FontsDict) -> None:
        self.texts: List[Text] = []
        self.buttons = [ButtonAnimate(button[0], button[1]) for button in STARTING_MENU['buttons']]

        for text in STARTING_MENU['texts']:
            self.texts.append(Text(
                fonts['default'] if not text['is_title'] else fonts['title'],
                text['text'],
                text['pos'],
                text['center_by'],
                bg=True,
                bg_offset_y=text['offset_y']
            ))

    def handle_btn_click(self) -> None:
        for button in self.buttons:
            if button.hovered:
                button.click()
                break

    def render(self, display_surf: Surface) -> None:
        for text in self.texts:
            display_surf.blit(text.surf, text.rect)

        mouse_pos = mouse.get_pos()
        for button in self.buttons:
            button.render(display_surf, mouse_pos)