import pygame as pg

from ..utils import load_img

class TextBackground(pg.sprite.Sprite):
    COLOR: pg.Color

    def __init__(self, rect: pg.Rect, all_bg: pg.sprite.Group, offset_y: int = 0, offset_x: int = 0) -> None:
        pg.sprite.Sprite.__init__(self, all_bg)

        self.image = pg.Surface(rect.size)
        self.image.fill(self.COLOR)

        self.rect = rect.copy()
        self.rect.move_ip(offset_x, offset_y)


class Text(pg.sprite.Sprite):
    COLOR: pg.Color

    def __init__(self, font: pg.font.Font, text: str, pos: tuple[int, int], rect_pos: str, all_text: pg.sprite.Group) -> None:
        pg.sprite.Sprite.__init__(self, all_text)

        self.image = font.render(text, True, self.COLOR)
    
        if rect_pos == 'midtop':
            self.rect = self.image.get_rect(midtop=pos)
        elif rect_pos == 'midbottom':
            self.rect = self.image.get_rect(midbottom=pos)


class Image(pg.sprite.Sprite):
    def __init__(self, file: str, pos: tuple[int, int], all_img: pg.sprite.Group) -> None:
        pg.sprite.Sprite.__init__(self, all_img)

        self.image = load_img(file, convert_a=True)
        self.rect = self.image.get_rect(bottomright=pos)