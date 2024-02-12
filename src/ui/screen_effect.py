from pygame import Surface, draw, transform
from src.const.settings import CRS_EFFECT
from random import randint


class CRS:
    """Simule a cathode ray screen"""
    def __init__(self, vignette: Surface) -> None:
        self.min_alpha = CRS_EFFECT['min_alpha']
        self.max_alpha = CRS_EFFECT['max_alpha']
        self.vignette = transform.scale(vignette, CRS_EFFECT['size'])

        line_gap = CRS_EFFECT['line_gap']
        line_amount = CRS_EFFECT['size'][1] // line_gap

        for line in range(line_amount):
            y = line * line_gap
            draw.line(
                self.vignette,
                CRS_EFFECT['line_color'],
                (0, y),
                (CRS_EFFECT['size'][0], y),
                1
            )
    
    def render(self, display_surf: Surface) -> None:
        self.vignette.set_alpha(randint(self.min_alpha, self.max_alpha))
        display_surf.blit(self.vignette, (0, 0))
        