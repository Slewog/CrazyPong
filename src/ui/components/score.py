import pygame as pg
from src.const.settings import HUD

class Score(pg.sprite.Sprite):
    FONT: pg.font.Font
    FONT_COLOR: pg.Color
    OFFSET_Y = HUD['score_offset_y']

    def __init__(self, pos_x: int, group: pg.sprite.Group) -> None:
        pg.sprite.Sprite.__init__(self, group)
        
        self.pos_x = pos_x
        self.current = int(4)
        self.update_surf()

    def update_surf(self) -> None:
        self.image = self.FONT.render(str(self.current), True, self.FONT_COLOR)
        self.rect = self.image.get_rect(midtop=(self.pos_x, self.OFFSET_Y))

    def reset(self) -> None:
        self.current = int(0)
        self.update_surf()

    def add_point(self) -> None:
        self.current += 1
        self.update_surf()