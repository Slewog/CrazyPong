import pygame as pg
from src.const.settings import HUD

class Score(pg.sprite.Sprite):
    FONT: pg.font.Font
    FONT_COLOR: pg.Color
    OFFSET_Y = HUD['score_offset_y']

    def __init__(self, pos_x, group) -> None:
        pg.sprite.Sprite.__init__(self, group)
        
        self.pos_x = pos_x
        self.current = 4
        self.update_surf()

    def update_surf(self):
        self.image = self.FONT.render(str(self.current), True, self.FONT_COLOR)
        self.rect = self.image.get_rect(midtop=(self.pos_x, self.OFFSET_Y))

    def reset(self):
        self.current = 0
        self.update_surf()

    def add_point(self):
        self.current += 1
        self.update_surf()