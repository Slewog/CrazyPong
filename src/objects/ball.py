from __future__ import annotations
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from .paddle import Paddle

import pygame as pg
from random import choice

from src.const.settings import BALL, SCREEN_RECT
from src.const.custom_event import CE_BALL_OUT_SCREEN


class Ball(pg.sprite.Sprite):
    MIN_COLL_TOL = BALL['min_coll_tol']
    MAX_COLL_TOL = BALL['max_coll_tol']
    VELOCITY = BALL['velocity']
    RADIUS = BALL['radius']
    SIZE = (RADIUS * 2, RADIUS * 2)
    SCREEN_RECT = SCREEN_RECT

    COLOR: pg.Color
    HIT_SOUND: pg.mixer.Sound

    def __init__(self, group: pg.sprite.GroupSingle) -> None:
        pg.sprite.Sprite.__init__(self, group)

        self.active = bool(False)

        self.direction = pg.math.Vector2(
            choice((self.VELOCITY, -self.VELOCITY)),
            choice((self.VELOCITY, -self.VELOCITY))
        )

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
        self.rect = self.image.get_rect(center=BALL['starting_pos'])
    
    def set_active(self, state: bool) -> None:
        if state == self.active or type(state) != bool:
            return
        self.active = state

    def reset(self, full: bool = False):
        self.rect.center = BALL['starting_pos']
        self.set_active(False)
        
        if not full:
            self.direction.x *= -1
            self.direction.y = int(choice((self.VELOCITY, -self.VELOCITY)))
        else:
            self.direction = pg.math.Vector2(
                choice((self.VELOCITY, -self.VELOCITY)),
                choice((self.VELOCITY, -self.VELOCITY))
            )

    def check_display_collisions(self, direction: str, new_pos: float) -> int | float:
        if direction == 'vertical':
            if self.rect.top + new_pos < 0:
                self.HIT_SOUND.play()
                new_pos = -self.rect.top
                self.direction.y *= -1

            if self.rect.bottom + new_pos > self.SCREEN_RECT.height:
                self.HIT_SOUND.play()
                new_pos = self.SCREEN_RECT.height - self.rect.bottom
                self.direction.y *= -1

        if direction == 'horizontal':
            target = None
            if self.rect.left + new_pos < 0:
                target = 'right'

            if self.rect.right + new_pos > self.SCREEN_RECT.width:
                target = 'left'
            
            pg.event.post(pg.event.Event(CE_BALL_OUT_SCREEN, {'target': target}))
        return new_pos

    def check_collisions(self, direction: str, paddles: List[Paddle], new_pos: float) -> int | float:
        overlap_paddles: List[Paddle] = []

        for paddle in paddles:
            if self.rect.colliderect(paddle.rect):
                overlap_paddles.append(paddle)

        if not overlap_paddles:
            return self.check_display_collisions(direction, new_pos)
        
        if direction == 'horizontal':
            for paddle in overlap_paddles:
                if self.direction.x < 0:
                    distance_left = abs(self.rect.left - paddle.rect.right)
                    
                    if distance_left < self.MAX_COLL_TOL and distance_left > self.MIN_COLL_TOL:
                        self.HIT_SOUND.play()
                        new_pos = distance_left
                        self.direction.x *= -1

                if self.direction.x > 0:
                    distance_right = abs(self.rect.right - paddle.rect.left)
                    
                    if distance_right < self.MAX_COLL_TOL and distance_right > self.MIN_COLL_TOL:
                        self.HIT_SOUND.play()
                        new_pos = -distance_right
                        self.direction.x *= -1
        
        if direction == 'vertical':
            for paddle in overlap_paddles:
                if self.direction.y > 0:
                    distance_top = abs(self.rect.bottom - paddle.rect.top)

                    if distance_top < self.MAX_COLL_TOL and distance_top > self.MIN_COLL_TOL:
                        self.HIT_SOUND.play()
                        new_pos = -distance_top
                        self.direction.y *= -1

                if self.direction.y < 0:
                    distance_bottom = abs((self.rect.top) - paddle.rect.bottom)
                    
                    if distance_bottom < self.MAX_COLL_TOL and distance_bottom > self.MIN_COLL_TOL:
                        self.HIT_SOUND.play()
                        new_pos = distance_bottom
                        self.direction.y *= -1

        return self.check_display_collisions(direction, new_pos)

    def update(self, dt: float, paddles: List[Paddle]) -> None:
        if not self.active:
            return

        dir_x, dir_y = int(0), int(0)

        dir_x = self.check_collisions('horizontal', paddles, self.direction.x * dt)
        dir_y = self.check_collisions('vertical', paddles, self.direction.y * dt)

        if dir_x != 0 or dir_y != 0:
            self.rect.move_ip(dir_x, dir_y)
