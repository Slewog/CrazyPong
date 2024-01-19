import pygame as pg
from sys import exit
from time import time

from .const.custom_event import CE_BTN_CLICKED
from .const.settings import GAME, FONT, COLORS
from .ui.menu import Menu

from .utils import load_color, ColorValue


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

        self.state = str('menu')
        self.current_level = None
        self.colors: dict[str, ColorValue] = {}

    def set_state(self, new_state: str):
        if self.state == new_state or type(new_state) != str:
            return
        
        if new_state == 'quit':
            self.quit()
        
        self.state = new_state

    def load_assets(self):
        for color_name, color in COLORS.items():
            self.colors[color_name] = load_color(color)

        self.menu.load(self.SCREEN_RECT, FONT, self.colors)

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
                if e.type == pg.QUIT:
                    self.set_state('quit')
                
                if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    self.set_state('menu')

                if self.state == 'menu' and e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                    self.menu.handle_btn_click()
                
                if e.type == CE_BTN_CLICKED:
                    if e.action == 'play':
                        print(e)
                    elif e.action == 'quit':
                        self.set_state('quit')

            current_time = time()
            dt = current_time - prev_dt
            prev_dt = current_time

            self.display_surf.fill(self.colors['background'])

            if self.state == 'menu':
                self.menu.render(self.display_surf)

            # Middle X
            pg.draw.line(self.display_surf, pg.Color("red"), (0, self.SCREEN_RECT.height // 2), (self.SCREEN_RECT.width, self.SCREEN_RECT.height // 2), 1)

            # Middle Y
            pg.draw.line(self.display_surf, pg.Color("red"), (self.SCREEN_RECT.width / 2, 0), (self.SCREEN_RECT.width / 2, self.SCREEN_RECT.height), 1)

            pg.display.flip()