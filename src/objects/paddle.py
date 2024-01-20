from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ball import Ball

import pygame as pg


class Paddle(pg.sprite.Sprite):
    WIDTH = int(12)
    HEIGHT = int(180)
    VELOCITY = int(500)
    WALL_OFFSET = int(10)

    COLOR: pg.Color
    SCREEN_RECT: pg.Rect
    SCREEN_CENTERY: int
    SCREEN_BOTTOM: int

    def __init__(self, side: str, paddles_group: pg.sprite.Group()) -> None:
        pg.sprite.Sprite.__init__(self, paddles_group)

        self.image = pg.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(self.COLOR)

        self.side = side
        if side == 'left':
            self.default_pos = (self.WALL_OFFSET, self.SCREEN_CENTERY)
        else:
            self.default_pos = (
                self.SCREEN_RECT.width - self.WIDTH - self.WALL_OFFSET,
                self.SCREEN_CENTERY
            )

        self.rect = self.image.get_rect(midleft=self.default_pos)
        self.pos = pg.math.Vector2(self.rect.topleft)
    
    def check_wall_collision(self, dir_y: float):
        if self.rect.top + dir_y < self.WALL_OFFSET:
            dir_y = -self.rect.top + self.WALL_OFFSET
        
        if self.rect.bottom + dir_y > self.SCREEN_BOTTOM:
            dir_y = self.SCREEN_BOTTOM - self.rect.bottom

        return dir_y
    
    def move(self, dir_y: float):
        if dir_y != 0:
            self.rect.move_ip(0, self.check_wall_collision(dir_y))


class PlayerPaddle(Paddle):
    def __init__(self, side: str, paddles_group: pg.sprite.Group()) -> None:
        super().__init__(side, paddles_group)

    def update(self, dt: float, keys: pg.key.ScancodeWrapper, ball: Ball) -> None:
        dir_y = int(0)

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

        self.move(dir_y * dt)


class AIPaddle(Paddle):
    def __init__(self, paddles_group: pg.sprite.Group()) -> None:
        super().__init__('right', paddles_group)

    def update(self, dt: float, keys: pg.key.ScancodeWrapper, ball: Ball):
        dir_y = int(0)

        if self.rect.top <= ball.rect.y:
            dir_y = self.VELOCITY
        elif self.rect.bottom >= ball.rect.y:
            dir_y = -self.VELOCITY

        self.move(dir_y * dt)