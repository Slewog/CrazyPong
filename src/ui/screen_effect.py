from typing import TypedDict
from random import randint
import pygame as pg

CRS_DICT  = TypedDict("crs", {
    'file': str,
    'vignette': pg.Surface,
    'line_gap': int,
    'line_color': pg.Color,
    'min_alpha': int,
    'max_alpha': int,
    'screen_rect': pg.Rect
})

class CRS:
    """Simule a cathode ray screen"""
    def __init__(self, data:CRS_DICT) -> None:
        self.min_alpha = data['min_alpha']
        self.max_alpha = data['max_alpha']
        self.vignette = pg.transform.scale(data['vignette'], data['screen_rect'].size)

        line_gap = data['line_gap']
        line_amount = data['screen_rect'].height // line_gap

        for line in range(line_amount):
            y = line * line_gap
            pg.draw.line(
                self.vignette,
                data['line_color'],
                (0, y),
                (data['screen_rect'].width, y),
                1
            )
    
    def render(self, display_surf: pg.Surface):
        self.vignette.set_alpha(randint(self.min_alpha, self.max_alpha))
        display_surf.blit(self.vignette, (0, 0))
        