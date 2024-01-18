import pygame as pg
from sys import exit
from time import time

from .const.settings import GAME, FONT
from .const.settings import OBJECT_COLOR, BACKGROUND_COLOR, FONT_COLOR
from .ui.menu import Menu

from .utils import load_color



class Pong:
    FPS = GAME['fps']
    SCREEN_RECT = pg.Rect(0, 0, GAME['width'], GAME['height'])

    def __init__(self) -> None:
        pg.mixer.pre_init(44100, -16, 2, 512)
        pg.init()

        self.clock = pg.time.Clock()

        self.display_surf = pg.display.set_mode((self.SCREEN_RECT.size))
        pg.display.set_caption(GAME['name'])

        self.menu = Menu()

    def load_assets(self):
        self.colors = {
            'font': load_color(FONT_COLOR),
            'objects': load_color(OBJECT_COLOR),
            'background': load_color(BACKGROUND_COLOR), 
        }

        FONT['color'] = self.colors['font']

        self.menu.load(self.SCREEN_RECT, FONT)

        self.display_surf.fill(self.colors['background'])
        pg.display.flip()

    def quit(self):
        pg.quit()
        exit()

    def run(self):
        self.load_assets()
        prev_dt = time()

        while True:
            self.clock.tick(self.FPS)

            for e in pg.event.get():
                if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    self.quit()

            current_time = time()
            dt = current_time - prev_dt
            prev_dt = current_time

            self.display_surf.fill(self.colors['background'])

            self.menu.render(self.display_surf)

            pg.display.flip()