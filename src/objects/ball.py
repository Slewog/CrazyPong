from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .paddle import Paddle

import pygame as pg
from random import choice, randint
from pygame.locals import SRCALPHA, BLEND_RGBA_MIN

from src.const.settings import BALL, SCREEN_RECT, CE_BALL_OUT_SCREEN


class Ball(pg.sprite.Sprite):
    BOOST = BALL['boost']
    VELOCITY = BALL['velocity']
    MAX_VELOCITY = BALL['max_vel']
    RADIUS = BALL['radius']
    SIZE = (RADIUS * 2, RADIUS * 2)
    SCREEN_RECT = SCREEN_RECT
    START_POS_Y_OFF = BALL['start_pos_offset']
    MAX_OUT = BALL['max_out']

    COLOR: pg.Color
    HIT_SOUND: pg.mixer.Sound

    def __init__(self, group: pg.sprite.GroupSingle) -> None:
        pg.sprite.Sprite.__init__(self, group)

        self.active = bool(False)

        self.direction = pg.math.Vector2(self.get_starting_vel(), self.get_starting_vel())

        # Ball surface.
        rect_image = pg.Surface(self.SIZE, SRCALPHA)
        pg.draw.rect(
            rect_image,
            (255, 255, 255),
            (0, 0, *self.SIZE),
            border_radius=self.RADIUS
        )

        self.image = pg.Surface(self.SIZE)
        self.image.fill(self.COLOR)
        self.image = self.image.convert_alpha()
        self.image.blit(rect_image, (0, 0), None, BLEND_RGBA_MIN)

        # Ball rect.
        self.rect = self.image.get_rect(center=self.get_random_start_pos())
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.old_rect = self.rect.copy()
        self.lock_y = bool(False)
    
    def set_active(self, state: bool) -> None:
        if state == self.active or type(state) != bool:
            return
        self.active = state

    def get_random_start_pos(self):
        return (
            self.SCREEN_RECT.centerx,
            randint(self.START_POS_Y_OFF, self.SCREEN_RECT.height - self.START_POS_Y_OFF)
        )

    def get_starting_vel(self):
        return choice((self.VELOCITY, -self.VELOCITY))
    
    def get_boost(self, vel):
        return self.BOOST if vel > 0 else -self.BOOST
    
    def speed_up(self):
        if abs(self.direction.x) < self.MAX_VELOCITY:
            self.direction.x += self.get_boost(self.direction.x)
        
        if abs(self.direction.y) < self.MAX_VELOCITY:
            self.direction.y += self.get_boost(self.direction.y)
    
    def reset(self, full: bool = False) -> None:
        self.rect.center = self.get_random_start_pos()
        self.pos.x = self.rect.x
        self.pos.y = self.rect.y
        self.set_active(False)
        
        if not full:
            self.direction.x *= -1
            self.direction.y = self.get_starting_vel()
        else:
            self.direction.x = self.get_starting_vel()
            self.direction.y = self.get_starting_vel()

    def check_display_collisions(self, direction: str) -> None:
        if direction == 'vertical':
            if self.direction.y < 0 and self.rect.top < 0:
                self.HIT_SOUND.play()
                self.rect.top = 0
                self.pos.y = self.rect.y
                self.direction.y *= -1

            if self.direction.y > 0 and self.rect.bottom > self.SCREEN_RECT.height:
                self.HIT_SOUND.play()
                self.rect.bottom = self.SCREEN_RECT.height
                self.pos.y = self.rect.y
                self.direction.y *= -1

        if direction == 'horizontal':
            if self.direction.x < 0 and self.rect.left < -self.MAX_OUT:
                pg.event.post(pg.event.Event(CE_BALL_OUT_SCREEN, {'target': 'right'}))

            if self.direction.x > 0 and self.rect.right > self.SCREEN_RECT.width + self.MAX_OUT:
                pg.event.post(pg.event.Event(CE_BALL_OUT_SCREEN, {'target': 'left'}))

    def check_collisions(self, direction: str, paddles: List[Paddle]) -> None:
        overlap_paddles = [paddle for paddle in paddles if self.rect.colliderect(paddle.rect)]

        if not overlap_paddles:
            self.lock_y = bool(False)
            self.check_display_collisions(direction)
            return 

        if overlap_paddles:
            for paddle in overlap_paddles:
                # Right collision.
                if self.rect.left <= paddle.rect.right and self.old_rect.left >= paddle.old_rect.right:
                    self.HIT_SOUND.play()
                    self.rect.left = paddle.rect.right
                    self.pos.x = self.rect.x
                    self.direction.x *= -1
                    self.speed_up()
                
                # Left collision.
                if self.rect.right >= paddle.rect.left and self.old_rect.right <= paddle.old_rect.left:
                    self.HIT_SOUND.play()
                    self.rect.right = paddle.rect.left - 1
                    self.pos.x = self.rect.x
                    self.direction.x *= -1
                    self.speed_up()

                # Top collision.
                if self.rect.bottom >= paddle.rect.top and self.old_rect.bottom <= paddle.old_rect.top:
                    if self.rect.top <= 0 and self.rect.left < paddle.rect.right and self.rect.right > paddle.rect.left:
                        self.rect.top = 0
                        self.pos.y = self.rect.y

                        paddle.rect.top =  self.rect.height
                        self.lock_y = bool(True)
                    else:
                        self.rect.bottom = paddle.rect.top - 1
                        self.pos.y = self.rect.y
                        self.direction.y *= -1

                # Bottom collision.
                if self.rect.top <= paddle.rect.bottom and self.old_rect.top >= paddle.old_rect.bottom:
                    if self.rect.bottom >= self.SCREEN_RECT.height and self.rect.left < paddle.rect.right and self.rect.right > paddle.rect.left:
                        self.rect.bottom = self.SCREEN_RECT.height
                        self.pos.y = self.rect.y

                        paddle.rect.bottom = self.SCREEN_RECT.height - self.rect.height
                        self.lock_y = bool(True)
                    else:
                        self.rect.top = paddle.rect.bottom + 1
                        self.pos.y = self.rect.y
                        self.direction.y *= -1

    def update(self, dt: float, paddles: List[Paddle]) -> None:
        self.old_rect = self.rect.copy()

        self.pos.x += self.direction.x * dt
        self.rect.x = round(self.pos.x) 
        self.check_collisions('horizontal', paddles)

        if not self.lock_y:
            self.pos.y += self.direction.y * dt
            self.rect.y = round(self.pos.y) 
        self.check_collisions('vertical', paddles)
