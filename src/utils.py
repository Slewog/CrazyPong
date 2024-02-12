import sys
from os import path
from pygame import Surface, font, mixer, image
from typing import Tuple

from .const.settings import BG_CLR, FONT_CLR

# Get absolute path to resource, works for dev and for PyInstaller.
def get_path(tmp_path: str):
    for exception in ['\\src', '\\_internal']:
        if exception in tmp_path:
            tmp_path = tmp_path.split(exception)[0]
    return tmp_path
MAIN_PATH = get_path(getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__))))
del sys # Delete sys from memory.

FONTS_DIR = path.join(MAIN_PATH, "assets", "fonts")
SOUNDS_DIR = path.join(MAIN_PATH, "assets", "sounds")
GRAPHICS_DIR = path.join(MAIN_PATH, "assets", "graphics")

def load_font(font_name: str, size: int, custom: bool = True):
    """Load the font from system if custom is False."""
    if not custom:
        return font.SysFont(font, size)
    
    return font.Font(path.join(FONTS_DIR, font_name), size)

def load_sound(file: str, vol: float = 0.5, sub_dir: str = '') -> mixer.Sound:
    """Return NoneSound to avoid errors if pygame mixer is not ready"""
    if not mixer or not mixer.get_init():
        return NoneSound()

    loaded_sound = mixer.Sound(path.join(SOUNDS_DIR, sub_dir, file))
    loaded_sound.set_volume(vol)
    return loaded_sound

def load_img(file: str, sub_dir: str = "", convert_a: bool = False) -> Surface:
    """
    Return a Surface if the file doesn't exist to avoid errors.
        convert_a: Convert with alpha
    """
    file_path = path.join(GRAPHICS_DIR, sub_dir, file)

    if convert_a:
        return image.load(file_path).convert_alpha()
    
    return image.load(file_path).convert()


class Text:
    """Create a text"""
    COLOR = FONT_CLR
    BG_COLOR = BG_CLR

    def __init__(self, font: font.Font, text: str, pos: Tuple[int, int], center_by: str,
                bg: bool = False, bg_offset_y: int = 0, bg_offset_x: int = 0) -> None:
        """
        center_by: 'midtop' | 'midbottom' | center
        bg: True if you want a bg behind the text.
        """

        txt = font.render(text, True, self.COLOR)
        self.surf = Surface(txt.get_size())

        if bg:
            self.surf.fill(self.BG_COLOR)

        self.surf.blit(txt, (0 + bg_offset_x, 0 + bg_offset_y))

        match center_by:
            case 'center':
                self.rect = self.surf.get_rect(center=pos)
            case 'midtop':
                self.rect = self.surf.get_rect(midtop=pos)
            case 'midbottom':
                self.rect = self.surf.get_rect(midbottom=pos)


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