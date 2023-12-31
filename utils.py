import sys
from os import path
import pygame as pg
from settings import DebugSettings

MAIN_DIR = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))

def resource_path(directory:str, resource:str) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    return path.join(MAIN_DIR, directory, resource)

def load_sound(file:str, vol:float=1.0) -> pg.mixer.Sound:
    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()
    
    d_path = str("assets/sounds")
    sound_path = resource_path(d_path, file)
    if not path.exists(sound_path):
        return NoneSound()
    
    loaded_sound = pg.mixer.Sound(sound_path)
    loaded_sound.set_volume(vol)
    return loaded_sound

def load_color(color:str) -> pg.Color:
    if type(color) == tuple:
            return color
    else:
        return pg.Color(color)


class NoneSound:
    def play(self):
        pass


class DebugTools:
    def __init__(self) -> None:
        self.data:list[str] = []
        self.font = pg.font.Font(None, DebugSettings.FONT_SIZE)
        self.border_radius = DebugSettings.BORDER_RADIUS

        self.rect = pg.Rect(DebugSettings.X_POS, DebugSettings.Y_POS, DebugSettings.WIDTH, DebugSettings.HEIGHT)

        self.font.set_underline(True)
        self.font.set_bold(True)
        self.font.set_italic(True)
        self.title = self.font.render('DEBUG TOOLS:', True, 'white')
        self.title_rect = self.title.get_rect(midtop = (self.rect.midtop[0], self.rect.midtop[1] + 10))
        self.font.set_underline(False)
        self.font.set_bold(False)

        self.offset = self.title_rect.bottom + 10

    def add_data(self, data:str):
        self.data.append(data)
    
    def render(self, display:pg.Surface):
        pg.draw.rect(display, 'Black', self.rect, border_radius=self.border_radius)
        display.blit(self.title, self.title_rect)

        offset = self.offset

        for data in self.data:
            data_txt = self.font.render(data, True, 'white')

            data_txt_rect = data_txt.get_rect(topleft = (self.rect.left + 10, offset))
            display.blit(data_txt, data_txt_rect)
            offset += data_txt_rect.height + 5
        
        self.data:list[str] = []