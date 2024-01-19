from __future__ import annotations # <-still need this.
from typing import TYPE_CHECKING

if TYPE_CHECKING: # <-try this,
    from .ball import Ball # <-if this is only for type hintin

import pygame as pg


class Paddle(pg.sprite.Sprite):
    WIDTH = int(12)
    HEIGHT = int(180)
    VELOCITY = int(500)
    WALL_OFFSET = int(10)

    COLOR: pg.Color
    SCREEN_RECT: pg.Rect
    SCREEN_CENTERY: int
    
    def __init__(self, side, screen_centery) -> None:
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(self.COLOR)

        self.side = side
        if side == 'left':
            self.default_pos = (self.WALL_OFFSET, screen_centery)
        else:
            self.default_pos = (self.SCREEN_RECT.width - self.WIDTH - self.WALL_OFFSET, screen_centery)

        self.rect = self.image.get_rect(midleft=self.default_pos)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.old_rect = self.rect.copy()


class Player(Paddle):
    def __init__(self, side, screen_centery) -> None:
        super().__init__(side, screen_centery)

    def update(self, dt: float, keys: pg.key.ScancodeWrapper) -> None:
        self.old_rect = self.rect.copy()

        dir_y = 0

        if self.side == 'left':
            if keys[pg.K_z]:
                dir_y = -self.VELOCITY
            elif keys[pg.K_s]:
                dir_y = self.VELOCITY

        if self.side == 'right':
            if keys[pg.K_UP]:
                dir_y = -self.VELOCITY
            elif keys[pg.K_DOWN]:
                dir_y = self.VELOCITY

        dir_y = dir_y * dt

        if self.rect.top + dir_y < self.WALL_OFFSET:
            dir_y = -self.rect.top + self.WALL_OFFSET

        bottom = self.SCREEN_RECT.height - self.WALL_OFFSET
        if self.rect.bottom + dir_y > bottom:
            dir_y = bottom - self.rect.bottom

        if dir_y != 0:
            self.rect.move_ip(0, dir_y)


class AI(Paddle):
    def __init__(self, side, screen_centery) -> None:
        super().__init__(side, screen_centery)

    def update(self, dt: float, ball: Ball):
        self.old_rect = self.rect.copy()
        dir_y = int(0)

        if self.rect.top < ball.rect.y:
            dir_y = self.VELOCITY
        elif self.rect.bottom > ball.rect.y:
            dir_y = -self.VELOCITY

        dir_y = dir_y * dt

        if self.rect.top + dir_y < self.WALL_OFFSET:
            dir_y = -self.rect.top + self.WALL_OFFSET

        bottom = self.SCREEN_RECT.height - self.WALL_OFFSET
        if self.rect.bottom + dir_y > bottom:
            dir_y = bottom - self.rect.bottom

        if dir_y != 0:
            self.rect.move_ip(0, dir_y)