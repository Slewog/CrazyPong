import pygame as pg
from sys import exit
from time import time


FPS = int(60)
SCREEN_RECT = pg.Rect(0, 0, 1280, 720)


# Debug Tool var.
TITLE = str("DEBUG TOOLS:")
BG_COLOR = pg.Color('black')
TXT_COLOR = pg.Color('white')
WIDTH = int(210)
HEIGHT = int(155)
X_POS = int(30)
Y_POS = int(20)
FONT_SIZE = int(25)
BORDER_RADIUS = int(10)

class DebugTool:
    BG_COLOR = BG_COLOR
    TXT_COLOR = TXT_COLOR

    def __init__(self, display:pg.Surface) -> None:
        self.display = display
        self.data:list[str] = []
        self.font = pg.font.Font(None, FONT_SIZE)
        self.border_radius = BORDER_RADIUS

        self.rect = pg.Rect(X_POS, Y_POS, WIDTH, HEIGHT)

        self.font.set_underline(True)
        self.font.set_bold(True)
        self.font.set_italic(True)
        self.title = self.font.render(TITLE, True, self.TXT_COLOR)
        self.title_rect = self.title.get_rect(midtop = (self.rect.midtop[0], self.rect.midtop[1] + 10))
        self.font.set_underline(False)
        self.font.set_bold(False)

        self.offset = self.title_rect.bottom + 10

    def add_data(self, data:str):
        self.data.append(data)
    
    def render(self):
        pg.draw.rect(self.display, self.BG_COLOR, self.rect, border_radius=self.border_radius)
        self.display.blit(self.title, self.title_rect)

        offset = self.offset

        for data in self.data:
            data_txt = self.font.render(data, True, self.TXT_COLOR)

            data_txt_rect = data_txt.get_rect(topleft = (self.rect.left + 10, offset))
            self.display.blit(data_txt, data_txt_rect)
            offset += data_txt_rect.height + 5
        
        self.data.clear()
