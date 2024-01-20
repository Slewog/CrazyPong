from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .paddle import Paddle

import pygame as pg
from random import choice

from src.const.settings import BALL


class Ball(pg.sprite.Sprite):
    COLLISION_TOL = BALL['collision_tol']
    VELOCITY = BALL['velocity']
    RADIUS = BALL['radius']
    SIZE = (RADIUS * 2, RADIUS * 2)


    START_POS: tuple[int, int]
    COLOR: pg.Color
    SCREEN_RECT: pg.Rect
    HIT_SOUND: pg.mixer.Sound

    def __init__(self, ball: pg.sprite.GroupSingle) -> None:
        pg.sprite.Sprite.__init__(self, ball)

        self.active = bool(True)

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
        self.rect = self.image.get_rect(center=self.START_POS)
        self.pos = pg.math.Vector2(self.rect.topleft)

    def check_display_collisions(self, direction: str, new_pos: float):
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
            if self.rect.left + new_pos < 0:
                new_pos = -self.rect.left
                self.direction.x *= -1

            if self.rect.right + new_pos > self.SCREEN_RECT.width:
                new_pos = self.rect.right - self.rect.right
                self.direction.x *= -1
        return new_pos

    def check_collisions(self, direction: str, paddles: list[Paddle], new_pos: float):
        overlap_paddles: list[Paddle] = []

        for paddle in paddles:
            if self.rect.colliderect(paddle.rect):
                overlap_paddles.append(paddle)

        if not overlap_paddles:
            return self.check_display_collisions(direction, new_pos)
        
        self.HIT_SOUND.play()
        
        if direction == 'horizontal':
            for paddle in overlap_paddles:
                if self.direction.x < 0:
                    distance_left = abs(self.rect.left - paddle.rect.right)

                    if distance_left < self.COLLISION_TOL:
                        new_pos = distance_left
                        self.direction.x *= -1

                if self.direction.x > 0:
                    distance_right = abs(self.rect.right - paddle.rect.left)

                    if distance_right < self.COLLISION_TOL:
                        new_pos = -distance_right
                        self.direction.x *= -1
        
        if direction == 'vertical':
            for paddle in overlap_paddles:
                if self.direction.y > 0:
                    distance_top = abs(self.rect.bottom - paddle.rect.top)

                    if distance_top < self.COLLISION_TOL:
                        new_pos = -distance_top
                        self.direction.y *= -1

                if self.direction.y < 0:
                    distance_bottom = abs((self.rect.top) - paddle.rect.bottom)
                    
                    if distance_bottom < self.COLLISION_TOL:
                        new_pos = distance_bottom
                        self.direction.y *= -1

        return self.check_display_collisions(direction, new_pos)

    def update(self, dt, paddles):
        if not self.active:
            return

        dir_x, dir_y = int(0), int(0)

        dir_x = self.check_collisions('horizontal', paddles, self.direction.x * dt)
        dir_y = self.check_collisions('vertical', paddles, self.direction.y * dt)

        if dir_x != 0 or dir_y != 0:
            self.rect.move_ip(dir_x, dir_y)
