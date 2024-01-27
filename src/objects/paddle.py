from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ball import Ball

import pygame as pg

from src.const.settings import PADDLE, SCREEN_RECT
from src.ui.components.score import Score


class Paddle(pg.sprite.Sprite):
    SCREEN_RECT =  SCREEN_RECT
    SCREEN_CENTERY = SCREEN_RECT.centery
    SCREEN_BOTTOM = SCREEN_RECT.height - PADDLE['offset_y']
    
    WIDTH = PADDLE['width']
    HEIGHT = PADDLE['height']
    VELOCITY = PADDLE['velocity']
    OFFSET_X = PADDLE['offset_x']
    OFFSET_Y = PADDLE['offset_y']
    MAX_SCORE = PADDLE['max_score']

    COLOR: pg.Color

    def __init__(self, side: str, paddle_type: str, hud_pos_x: int, group: pg.sprite.Group) -> None:
        pg.sprite.Sprite.__init__(self, group)

        self.type = paddle_type
        self.cur_vel = int(0)
        self.score = Score(hud_pos_x, group)

        self.side = side
        if side == 'left':
            self.default_pos = (self.OFFSET_X, self.SCREEN_CENTERY)
        else:
            self.default_pos = (
                self.SCREEN_RECT.width - self.WIDTH - self.OFFSET_X,
                self.SCREEN_CENTERY
            )
        self.image = pg.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(self.COLOR)
        self.rect = self.image.get_rect(midleft=self.default_pos)

    def winned(self) -> bool:
        return self.score.current >= self.MAX_SCORE
    
    def reset(self) -> None:
        self.reset_velocity()
        self.rect.midleft = self.default_pos
        self.score.reset()

    def reset_velocity(self) -> None:
        self.cur_vel = int(0)

    def destroy(self) -> None:
        self.score.kill()
        self.kill()
    
    def check_wall_collision(self, dir_y: float) -> int | float:
        if self.rect.top + dir_y < self.OFFSET_Y:
            dir_y = -self.rect.top + self.OFFSET_Y
        
        if self.rect.bottom + dir_y > self.SCREEN_BOTTOM:
            dir_y = self.SCREEN_BOTTOM - self.rect.bottom

        return dir_y
    
    def check_input(self, keys: pg.key.ScancodeWrapper) -> None:
        self.cur_vel = int(0)

        if self.side == 'left':
            if keys[pg.K_r]:
                self.cur_vel = -self.VELOCITY
            elif keys[pg.K_f]:
                self.cur_vel = self.VELOCITY

        if self.side == 'right':
            if keys[pg.K_UP]:
                self.cur_vel = -self.VELOCITY
            elif keys[pg.K_DOWN]:
                self.cur_vel = self.VELOCITY
    
    def update(self, dt: float, ball: Ball) -> None:
        if self.type == 'ai':
            dist = self.rect.centery - ball.rect.centery
            ai_speed = self.VELOCITY * dt
            if abs(dist) > ai_speed:
                self.rect.move_ip(
                    0,
                    self.check_wall_collision(
                        -1 * (ai_speed * (dist / abs(dist)))
                    )
                )

        if self.type == 'player' and self.cur_vel != 0:
            self.rect.move_ip(0, self.check_wall_collision(self.cur_vel * dt))