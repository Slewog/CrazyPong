from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ball import Ball

import pygame as pg

from src.const.settings import PADDLE
from src.ui.components.score import Score


class Paddle(pg.sprite.Sprite):
    WIDTH = PADDLE['width']
    HEIGHT = PADDLE['height']
    VELOCITY = PADDLE['velocity']
    AI_VELOCITY = VELOCITY - PADDLE['ai_vel_debuff']
    OFFSET_X = PADDLE['offset_x']
    OFFSET_Y = PADDLE['offset_y']
    MAX_SCORE = PADDLE['max_score']

    COLOR: pg.Color
    SCREEN_RECT: pg.Rect
    SCREEN_CENTERY: int
    SCREEN_BOTTOM: int

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

    def winned(self):
        return self.score.current >= self.MAX_SCORE
    
    def reset(self):
        self.cur_vel = int(0)
        self.rect.midleft = self.default_pos
        self.score.reset()

    def destroy(self):
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
            if keys[pg.K_z]:
                self.cur_vel = -self.VELOCITY
            elif keys[pg.K_s]:
                self.cur_vel = self.VELOCITY

        if self.side == 'right':
            if keys[pg.K_UP]:
                self.cur_vel = -self.VELOCITY
            elif keys[pg.K_DOWN]:
                self.cur_vel = self.VELOCITY
    
    def update(self, dt: float, ball: Ball) -> None:
        dir_y = int(0)

        if self.type == 'ai' and ball.active:
            if self.rect.centery < ball.rect.top:
                dir_y = self.AI_VELOCITY
            
            if self.rect.centery > ball.rect.bottom:
                dir_y = -self.AI_VELOCITY
                
        if self.type == 'player':
            dir_y = self.cur_vel
        
        if dir_y != 0:
            self.rect.move_ip(0, self.check_wall_collision(dir_y * dt))
