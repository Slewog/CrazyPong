import sys
from os import path
import pygame as pg

MAIN_DIR = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))

def resource_path(directory: str, resource: str) -> str:
    return path.join(MAIN_DIR, directory, resource)

def load_sound(file: str, vol: float = 1.0) -> pg.mixer.Sound:
    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    d_path = str("assets/sounds")
    sound_path = resource_path(d_path, file)
    if not path.exists(sound_path):
        return NoneSound()

    loaded_sound = pg.mixer.Sound(sound_path)
    loaded_sound.set_volume(vol)
    return loaded_sound

def load_color(color: str | tuple[int, int, int]) -> pg.Color:
    if type(color) == tuple:
        return color

    return pg.Color(color)

class NoneSound:
    def play(self):
        pass
