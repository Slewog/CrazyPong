from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .objects.ball import Ball

import pygame as pg

from .const.settings import HUD, SCREEN_RECT
from .objects.paddle import Paddle
from .utils import Text
from .ui.components.buttons import ButtonAnimate

class Level:
    WIN_TXT_POS = (
        SCREEN_RECT.centerx,
        SCREEN_RECT.height // 2 - HUD['winner_msg_offset']
    )

    COUNTER_POS = (SCREEN_RECT.centerx, HUD['counter_pos_y'])
    COUNT_BG_OFFSET = HUD['counter_bg_offset']
    SCREEN_W_QUART = SCREEN_RECT.centerx // 2
    
    FONT: pg.font.Font
    FONT_COLOR: pg.Color
    BG_COLOR: pg.Color
    BUTTONS: List[ButtonAnimate]
    
    SCORE_SOUND: pg.mixer.Sound
    WIN_SOUND: pg.mixer.Sound
    
    def __init__(self, level_type: str, ball: Ball, ball_group: pg.sprite.GroupSingle) -> None:
        self.hud_group = pg.sprite.Group()
        self.ball_group = ball_group
        self.paddles_group = pg.sprite.Group()

        self.winned = bool(False)
        self.started = bool(False)
        self.counter = int(-1)
        self.reset_time = int(0)

        self.ball = ball
        self.paddles = [
            Paddle('left', 'player', self.SCREEN_W_QUART, self.paddles_group),
            Paddle('right', 'ai' if level_type == 'oneplayer' else 'player', self.SCREEN_W_QUART * 3, self.paddles_group)
        ]

    def reset(self) -> None:
        for paddle in self.paddles:
            paddle.reset()
        
        self.winned = bool(False)

        if getattr(self, 'win_text', None):
            self.win_text.destroy()

        self.reset_time = pg.time.get_ticks()

        self.ball.reset(True)

    def start(self) -> None:
        self.started = not self.started
        self.reset_time = pg.time.get_ticks()

    def destroy(self) -> None:
        self.ball.reset(True)

        if getattr(self, 'win_text', None):
            self.win_text.destroy()

        for paddle in self.paddles:
            paddle.destroy()
        
    def add_point_to_paddle(self, target: str) -> None:
        """target is the side of the paddle targetted"""
        if type(target) != str: return

        for paddle in self.paddles:
            if paddle.side == target:
                paddle.score.add_point()
                winned = paddle.winned()

                if not winned:
                    self.reset_time = pg.time.get_ticks()
                    self.SCORE_SOUND.play()

                if winned:
                    self.winned = winned
                    self.win_text = Text(
                        self.FONT,
                        "The AI is the winner" if paddle.type == 'ai' else f"The player {paddle.side} is the winner",
                        self.WIN_TXT_POS,
                        'center',
                        self.hud_group,
                        bg=True,
                        bg_offset_y= -2
                    )

                    for paddle in self.paddles:
                        paddle.reset_velocity()
                    
                    self.WIN_SOUND.play()
                
                self.ball.reset(self.winned)
                break
    
    def counter_active(self) -> bool:
        return self.reset_time != 0
    
    def update_counter(self, value: int) -> None:
        self.counter = value

        self.counter_txt = self.FONT.render(str(self.counter), True, self.FONT_COLOR)
        self.counter_rect = self.counter_txt.get_rect(midbottom=self.COUNTER_POS)

        self.counter_bg = self.counter_rect.copy()
        self.counter_bg.move_ip(0, -self.COUNT_BG_OFFSET)

    def check_counter(self) -> None:
        reset_time = pg.time.get_ticks() - self.reset_time

        if reset_time <= 700 and self.counter != 3:
            self.update_counter(3)
        elif 700 < reset_time <= 1400 and self.counter != 2:
            self.update_counter(2)
        elif 1400 < reset_time <= 2100 and self.counter != 1:
            self.update_counter(1)
        elif reset_time >= 2100:
            self.ball.set_active(True)
            self.reset_time = int(0)
            self.update_counter(-1)
    
    def handle_btn_click(self) -> None:
        for button in self.BUTTONS:
            if button.hovered:
                button.click()
                break

    def render_frame(self, display_surf: pg.Surface) -> None:
        self.paddles_group.draw(display_surf)
        self.hud_group.draw(display_surf)
        
        if self.winned:
            mouse_pos = pg.mouse.get_pos()
            for button in self.BUTTONS:
                button.render(display_surf, mouse_pos)
            
            return

        if self.counter_active():
            pg.draw.rect(display_surf, self.BG_COLOR, self.counter_bg)
            self.ball_group.draw(display_surf)
            display_surf.blit(self.counter_txt, self.counter_rect)
            return
        
        self.ball_group.draw(display_surf)

    def run(self, display_surf: pg.Surface, dt: float) -> None:
        if not self.winned:
            keys = pg.key.get_pressed()
            for paddle in self.paddles:
                paddle.check_input(keys)
            
            if self.counter_active():
                self.check_counter()

        self.paddles_group.update(dt, self.ball)
        
        if self.ball.active:
            self.ball_group.update(dt, self.paddles)

        self.render_frame(display_surf)