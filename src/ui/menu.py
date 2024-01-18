from typing import Any
import pygame as pg

from ..const.settings import MENU
from ..const.locales import COPYRIGHT
from ..utils import load_font
from .button import Button


class Menu:

    def __init__(self) -> None:
        self.buttons: list[Button] = []

        self.copyright = None

    def load(self, screen_rect: pg.Rect, font_data: dict[str, Any]):
        font = load_font(font_data['family'], font_data['size'])

        self.copyright_surf = font.render(COPYRIGHT, True, font_data['color'])
        self.copyright_rect = self.copyright_surf.get_rect(midbottom = (screen_rect.width // 2, screen_rect.height - 20))

    def render(self, display_surf: pg.Surface):
        display_surf.blit(self.copyright_surf, self.copyright_rect)
