from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .paddle import Paddle

import pygame as pg
from random import choice, randint

from src.const.settings import BALL, SCREEN_RECT, CE_BALL_OUT_SCREEN


class Ball(pg.sprite.Sprite):
    MIN_COLL_TOL = BALL['min_coll_tol']
    MAX_COLL_TOL = BALL['max_coll_tol']
    BOOST = BALL['boost']
    VELOCITY = BALL['velocity']
    MAX_VELOCITY = BALL['max_vel']
    RADIUS = BALL['radius']
    SIZE = (RADIUS * 2, RADIUS * 2)
    SCREEN_RECT = SCREEN_RECT
    START_POS_Y_OFF = BALL['start_pos_offset']

    COLOR: pg.Color
    HIT_SOUND: pg.mixer.Sound

    def __init__(self, group: pg.sprite.GroupSingle) -> None:
        pg.sprite.Sprite.__init__(self, group)

        self.active = bool(False)

        self.direction = pg.math.Vector2(self.get_starting_vel(), self.get_starting_vel())

        # Ball surface.
        rect_image = pg.Surface(self.SIZE, pg.SRCALPHA)
        pg.draw.rect(
            rect_image,
            (255, 255, 255),
            (0, 0, *self.SIZE),
            border_radius=self.RADIUS
        )

        self.image = pg.Surface(self.SIZE)
        self.image.fill(self.COLOR)
        self.image = self.image.convert_alpha()
        self.image.blit(rect_image, (0, 0), None, pg.BLEND_RGBA_MIN)

        # Ball rect.
        self.rect = self.image.get_rect(center=self.get_random_start_pos())
    
    def set_active(self, state: bool) -> None:
        if state == self.active or type(state) != bool:
            return
        self.active = state

    def get_random_start_pos(self):
        return (
            self.SCREEN_RECT.centerx,
            randint(self.START_POS_Y_OFF, self.SCREEN_RECT.height - self.START_POS_Y_OFF)
        )

    def get_starting_vel(self, cur_vel: int = None):
        if cur_vel is not None:
            cur_vel = abs(cur_vel)
            return choice((cur_vel, -cur_vel))
    
        return choice((self.VELOCITY, -self.VELOCITY))
    
    def get_boost(self, vel):
        return self.BOOST if vel > 0 else -self.BOOST
    
    def can_speed_up(self):
        return abs(self.direction.x) < self.MAX_VELOCITY and abs(self.direction.y) < self.MAX_VELOCITY
    
    def reset(self, full: bool = False) -> None:
        self.rect.center = self.get_random_start_pos()
        self.set_active(False)
        
        if not full:
            self.direction.x *= -1
            self.direction.y = self.get_starting_vel(self.direction.y)
        else:
            self.direction.x = self.get_starting_vel()
            self.direction.y = self.get_starting_vel()

    def check_display_collisions(self, direction: str, new_pos: float) -> int | float:
        if direction == 'vertical':
            if self.direction.y < 0 and self.rect.top + new_pos < 0:
                self.HIT_SOUND.play()
                new_pos = -self.rect.top
                self.direction.y *= -1

            if self.direction.y > 0 and self.rect.bottom + new_pos > self.SCREEN_RECT.height:
                self.HIT_SOUND.play()
                new_pos = self.SCREEN_RECT.height - self.rect.bottom
                self.direction.y *= -1

        if direction == 'horizontal':
            if self.direction.x < 0 and self.rect.left + new_pos < 0:
                pg.event.post(pg.event.Event(CE_BALL_OUT_SCREEN, {'target': 'right'}))

            if self.direction.x > 0 and self.rect.right + new_pos > self.SCREEN_RECT.width:
                pg.event.post(pg.event.Event(CE_BALL_OUT_SCREEN, {'target': 'left'}))

        return new_pos

    def check_collisions(self, direction: str, paddles: List[Paddle], new_pos: float) -> int | float:
        overlap_paddles = [paddle for paddle in paddles if self.rect.colliderect(paddle.rect)]
    
        if not overlap_paddles:
            return self.check_display_collisions(direction, new_pos)
        
        if direction == 'horizontal':
            for paddle in overlap_paddles:
                if self.direction.x < 0:
                    distance_left = abs(self.rect.left - paddle.rect.right)

                    if self.MIN_COLL_TOL < distance_left < self.MAX_COLL_TOL:
                        self.HIT_SOUND.play()
                        new_pos = distance_left
                        self.direction.x *= -1
                        
                        if self.can_speed_up():
                            self.direction.x += self.get_boost(self.direction.x)
                            self.direction.y += self.get_boost(self.direction.y)

                if self.direction.x > 0:
                    distance_right = abs(self.rect.right - paddle.rect.left)
                    
                    if self.MIN_COLL_TOL < distance_right < self.MAX_COLL_TOL:
                        self.HIT_SOUND.play()
                        new_pos = -distance_right
                        self.direction.x *= -1

                        if self.can_speed_up():
                            self.direction.x += self.get_boost(self.direction.x)
                            self.direction.y += self.get_boost(self.direction.y)
        
        if direction == 'vertical':
            for paddle in overlap_paddles:
                if self.direction.y > 0:
                    distance_top = abs(self.rect.bottom - paddle.rect.top)

                    if self.MIN_COLL_TOL < distance_top < self.MAX_COLL_TOL:
                        self.HIT_SOUND.play()
                        new_pos = -distance_top
                        self.direction.y *= -1

                if self.direction.y < 0:
                    distance_bottom = abs((self.rect.top) - paddle.rect.bottom)
                    
                    if self.MIN_COLL_TOL < distance_bottom < self.MAX_COLL_TOL:
                        self.HIT_SOUND.play()
                        new_pos = distance_bottom
                        self.direction.y *= -1

        return self.check_display_collisions(direction, new_pos)

    def update(self, dt: float, paddles: List[Paddle]) -> None:
        dir_x, dir_y = int(0), int(0)

        dir_x = self.check_collisions('horizontal', paddles, self.direction.x * dt)
        dir_y = self.check_collisions('vertical', paddles, self.direction.y * dt)

        if dir_x != 0 or dir_y != 0:
            self.rect.move_ip(dir_x, dir_y)
