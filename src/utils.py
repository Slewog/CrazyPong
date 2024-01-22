
import sys
from os import path
from typing import Tuple
import pygame as pg

from .const.custom_typing import ColorValue

# Get absolute path to resource, works for dev and for PyInstaller.
MAIN_PATH = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__))).split("\\src")[0]
del sys # Delete sys from memory.

# Create all dir path
FONTS_DIR = path.join(MAIN_PATH, "assets", "fonts")
SOUNDS_DIR = path.join(MAIN_PATH, "assets", "sounds")
GRAPHICS_DIR = path.join(MAIN_PATH, "assets", "graphics")


def load_color(color: ColorValue) -> pg.Color:
    """color: str | Tuple[int, int, int] | List[int]"""
    if type(color) == tuple:
        return color

    if type(color) == list:
        return tuple(color)

    return pg.Color(color)

def load_font(font: str, size: int, from_system: bool = False) -> pg.font.Font:
    """Return the default font to avoid errors if the font doesn't exist."""
    if from_system:
        return pg.font.SysFont(font, size)

    font_path = path.join(FONTS_DIR, font)
    if not path.exists(font_path):
        return pg.font.SysFont(None, size)

    return pg.font.Font(font_path, size)

def load_sound(file: str, vol: float = 1.0, sub_dir: str = "") -> pg.mixer.Sound:
    """Return NoneSound to avoid errors if the file doesn't exist"""
    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    file_path = path.join(SOUNDS_DIR, sub_dir, file)

    if not path.exists(file_path):
        return NoneSound()

    loaded_sound = pg.mixer.Sound(file_path)
    loaded_sound.set_volume(vol)
    return loaded_sound

def load_img(file: str, sub_dir: str = "", convert_a: bool = False, convert: bool = False) -> pg.Surface:
    """
    Return a Surface if the file doesn't exist to avoid errors.
        convert: Convert without alpha
        convert_a: Convert with alpha
        scale: int | float | '2x' |Tuple[int, int]
    """
    file_path = path.join(GRAPHICS_DIR, sub_dir, file)

    if not path.exists(file_path):
        img = pg.Surface((50, 50))
    else:
        img = pg.image.load(file_path)

    if convert_a:
        img = img.convert_alpha()
    elif convert:
        img = img.convert()

    return img


class RectBackground(pg.sprite.Sprite):
    """Create a background from a rect as sprite to render in a group"""
    COLOR: pg.Color

    def __init__(self, rect: pg.Rect, group: pg.sprite.Group, offset_y: int = 0, offset_x: int = 0) -> None:
        pg.sprite.Sprite.__init__(self, group)

        self.image = pg.Surface(rect.size)
        self.image.fill(self.COLOR)

        self.rect = rect.copy()
        self.rect.move_ip(offset_x, offset_y)


class Text(pg.sprite.Sprite):
    """Create a text as sprite to render in a group"""
    COLOR: pg.Color

    def __init__(self, font: pg.font.Font, text: str, pos: Tuple[int, int], center_by: str, group: pg.sprite.Group, bg: bool = False, bg_offset_y: int = 0, bg_offset_x: int = 0) -> None:
        """
        center_by: 'midtop' or 'midbottom'
        bg: True if you want a bg behind the text.
        """
        self.image = font.render(text, True, self.COLOR)

        if center_by == 'midtop':
            self.rect = self.image.get_rect(midtop=pos)
        elif center_by == 'midbottom':
            self.rect = self.image.get_rect(midbottom=pos)

        if bg:
            RectBackground(self.rect, group, bg_offset_y, bg_offset_x)

        pg.sprite.Sprite.__init__(self, group)


class Image(pg.sprite.Sprite):
    """Create a img as sprite to render in a group"""
    def __init__(self, file: str, pos: Tuple[int, int], group: pg.sprite.Group) -> None:
        pg.sprite.Sprite.__init__(self, group)

        self.image = load_img(file, convert_a=True)
        self.rect = self.image.get_rect(bottomright=pos)


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