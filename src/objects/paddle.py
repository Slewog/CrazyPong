from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ball import Ball

import pygame as pg
from pygame.locals import K_r, K_f, K_UP, K_DOWN

from src.const.settings import PADDLE, SCREEN_RECT,  HUD

class Score(pg.sprite.Sprite):
    FONT: pg.font.Font
    FONT_COLOR: pg.Color
    OFFSET_Y = HUD['score_offset_y']

    def __init__(self, pos_x: int, group: pg.sprite.Group) -> None:
        pg.sprite.Sprite.__init__(self, group)
        
        self.pos_x = pos_x
        self.current = int(0)
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
        self.old_rect = self.rect.copy()

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
    
    def clamp_in_screen(self) -> None:
        if self.rect.top < self.OFFSET_Y:
            self.rect.top = self.OFFSET_Y
        
        if self.rect.bottom > self.SCREEN_BOTTOM:
            self.rect.bottom = self.SCREEN_BOTTOM
    
    def check_input(self, keys: pg.key.ScancodeWrapper) -> None:
        self.cur_vel = int(0)

        if self.side == 'left':
            if keys[K_r]:
                self.cur_vel = -self.VELOCITY
            elif keys[K_f]:
                self.cur_vel = self.VELOCITY

        if self.side == 'right':
            if keys[K_UP]:
                self.cur_vel = -self.VELOCITY
            elif keys[K_DOWN]:
                self.cur_vel = self.VELOCITY
    
    def update(self, dt: float, ball: Ball) -> None:
        self.old_rect = self.rect.copy()
        
        if self.type == 'ai':
            dist = self.rect.centery - ball.rect.centery
            ai_speed = self.VELOCITY * dt
            if abs(dist) > ai_speed:
                self.rect.y += -1 * (ai_speed * (dist / abs(dist)))
                self.clamp_in_screen()

        if self.type == 'player' and self.cur_vel != 0:
            self.rect.y += self.cur_vel * dt
            self.clamp_in_screen()