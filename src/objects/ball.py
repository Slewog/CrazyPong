from __future__ import annotations # <-still need this.
from typing import TYPE_CHECKING

if TYPE_CHECKING: # <-try this,
    from .paddle import Paddle # <-if this is only for type hintin

import pygame as pg
from random import choice

from ..const.settings import BALL


class Ball(pg.sprite.Sprite):
    VELOCITY = BALL['velocity']
    RADIUS = BALL['radius']
    SIZE = (RADIUS * 2, RADIUS * 2)

    START_POS: tuple[int, int]
    COLOR: pg.Color
    SCREEN_RECT: pg.Rect

    def __init__(self, paddle_left: Paddle, paddle_right: Paddle, ball_group: pg.sprite.GroupSingle(), all: pg.sprite.Group()) -> None:
        pg.sprite.Sprite.__init__(self, ball_group, all)

        self.paddle_left = paddle_left
        self.paddle_right = paddle_right

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

    def display_collisions(self, direction: str, new_pos: float):
        if direction == 'vertical':
            if self.rect.top + new_pos < 0:
                new_pos = -self.rect.top
                self.direction.y *= -1

            if self.rect.bottom + new_pos > self.SCREEN_RECT.height:
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

    def collisions(self, direction: str, new_pos: float):
        overlap_paddles: list[Paddle] = []

        if self.rect.colliderect(self.paddle_left.rect):
            overlap_paddles.append(self.paddle_left)
        if self.rect.colliderect(self.paddle_right.rect):
            overlap_paddles.append(self.paddle_right)

        if overlap_paddles:
            if direction == 'horizontal':
                for paddle in overlap_paddles:

                    distance_left = abs(self.rect.left - paddle.rect.right)
                    if distance_left < 10 and self.direction.x < 0:
                        new_pos = distance_left
                        self.direction.x *= -1

                    distance_right = abs(self.rect.right - paddle.rect.left)
                    if distance_right < 10 and self.direction.x > 0:
                        new_pos = -distance_right
                        self.direction.x *= -1
            
            if direction == 'vertical':
                for paddle in overlap_paddles:
                    
                    distance_top = abs(self.rect.bottom - paddle.rect.top)
                    if distance_top < 10 and self.direction.y > 0:
                        new_pos = -distance_top
                        self.direction.y *= -1

                    distance_bottom = abs((self.rect.top) - paddle.rect.bottom)
                    if distance_bottom < 10 and self.direction.y < 0:
                        new_pos = distance_bottom
                        self.direction.y *= -1
        return self.display_collisions(direction, new_pos)

    def update(self, dt):
        dir_x, dir_y = int(0), int(0)

        dir_x = self.collisions('horizontal', self.direction.x * dt)
        dir_y = self.collisions('vertical', self.direction.y * dt)

        if dir_x != 0 or dir_y != 0:
            self.rect.move_ip(dir_x, dir_y)
