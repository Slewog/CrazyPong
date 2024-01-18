from typing import Union, Tuple, List

from os import path
import pygame as pg

ColorValue = Union[str, Tuple[int, int, int], List[int]]

sounds_dir: str = None
fonts_dir: str = None

def set_path(main_dir: str):
    global sounds_dir, fonts_dir
    sounds_dir = path.join(main_dir, "assets", "sounds")
    fonts_dir = path.join(main_dir, "assets", "fonts")

def load_color(color: ColorValue) -> pg.Color:
    """color: str | tuple[int, int, int] | list[int]"""
    if type(color) == tuple:
        return color

    if type(color) == list:
        return tuple(color)

    return pg.Color(color)

def load_font(font: str, size: int, from_system: bool = False):
    """Return the default font to avoid errors if the font doesn't exist."""
    if from_system:
        return pg.font.SysFont(font, size)

    font_path = path.join(fonts_dir, font)
    if not path.exists(font_path):
        return pg.font.SysFont(None, size)

    return pg.font.Font(font_path, size)


class NoneSound:
    """Fake sound class to avoid errors"""

    def play(self):
        pass

    def stop(self):
        pass

    def fadeout(self, time: int):
        pass

    def set_volume(self, vol: float):
        pass

    def get_volume(self) -> float:
        pass

    def get_length(self) -> float:
        pass

    def get_raw(self) -> bytes:
        pass

    def get_num_channels(self) -> int:
        pass