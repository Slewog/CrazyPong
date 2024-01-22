import pygame as pg
from typing import List

from .const.settings import HUD
from .objects.paddle import Paddle
from .objects.ball import Ball
from .utils import Text
from .ui.components.buttons import ButtonAnimate

class Level:
    COUNTER_OFFSET_Y = HUD['counter_offset_y']
    COUNT_BG_OFFSET = HUD['counter_bg_offset']
    
    FONT: pg.font.Font
    FONT_COLOR: pg.Color
    BG_COLOR: pg.Color
    BUTTONS: List[ButtonAnimate]

    SCREEN_MW: int
    SCREEN_W_QUART: int
    WIN_TXT_POS: int
    SCORE_SOUND: pg.mixer.Sound
    WIN_SOUND: pg.mixer.Sound
    
    def __init__(self, level_type: str, debug) -> None:
        self.hud_group = pg.sprite.Group()
        self.ball_group = pg.sprite.GroupSingle()
        self.paddles_group = pg.sprite.Group()

        self.winned = bool(False)
        self.started = bool(False)
        self.counter = int(-1)
        self.reset_time = int(0)

        self.ball = Ball(self.ball_group)
        self.paddles = [
            Paddle('left', 'player', self.SCREEN_W_QUART, self.paddles_group),
            Paddle('right', level_type == 'oneplayer' and 'ai' or 'player', self.SCREEN_W_QUART * 3, self.paddles_group)
        ]

    def reset(self):
        for paddle in self.paddles:
            paddle.reset()
        
        self.winned = bool(False)

        if getattr(self, 'win_text', None):
            self.win_text.destroy()

        self.reset_time = pg.time.get_ticks()

    def start(self):
        self.started = not self.started
        self.reset_time = pg.time.get_ticks()

    def destroy(self) -> None:
        self.ball.kill()

        if getattr(self, 'win_text', None):
            self.win_text.destroy()

        for paddle in self.paddles:
            paddle.destroy()
        
    def add_point_to_paddle(self, target: str) -> None:
        """target is the side of the paddle targetted"""
        if type(target) != str:
            return

        for paddle in self.paddles:
            if paddle.side == target:
                paddle.score.add_point()
                winned = paddle.winned()

                if not winned:
                    self.reset_time = pg.time.get_ticks()
                    self.SCORE_SOUND.play()

                if winned:
                    if paddle.type == 'ai':
                        winner = "The AI is the winner"
                    else:
                        winner = f"The player {paddle.side} is the winner"

                    self.winned = winned
                    self.win_text = Text(
                        self.FONT,
                        winner,
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
    
    def counter_active(self):
        return self.reset_time != 0
    
    def update_counter(self, value: int) -> None:
        self.counter = value

        self.counter_txt = self.FONT.render(str(self.counter), True, self.FONT_COLOR)
        self.counter_rect = self.counter_txt.get_rect(
            midbottom = (self.SCREEN_MW, self.ball.rect.top - self.COUNTER_OFFSET_Y)
        )

        self.counter_bg = pg.Rect(
            self.counter_rect.x,
            self.counter_rect.y - self.COUNT_BG_OFFSET,
            self.counter_rect.width,
            self.counter_rect.height
        )

    def check_counter(self):
        current_time = pg.time.get_ticks()
        reset_time = current_time - self.reset_time

        if reset_time <= 700 and self.counter != 3:
            self.update_counter(3)
        if 700 < reset_time <= 1400 and self.counter != 2:
            self.update_counter(2)
        if 1400 < reset_time <= 2100 and self.counter != 1:
            self.update_counter(1)
        if reset_time >= 2100:
            self.ball.set_active(True)
            self.reset_time = int(0)
            self.update_counter(-1)
    
    def handle_btn_click(self):
        for button in self.BUTTONS:
            if button.hovered:
                button.click()

    def render_frame(self, display_surf: pg.Surface) -> None:
        self.paddles_group.draw(display_surf)
        self.ball_group.draw(display_surf)
        self.hud_group.draw(display_surf)

        if self.winned:
            mouse_pos = pg.mouse.get_pos()
            for button in self.BUTTONS:
                button.check_hover(mouse_pos)
                button.check_click()
                button.draw(display_surf)

        if not self.winned and self.counter_active():
            pg.draw.rect(display_surf, self.BG_COLOR, self.counter_bg)
            display_surf.blit(self.counter_txt, self.counter_rect)

    def run(self, display_surf: pg.Surface, dt: float) -> None:
        if not self.winned:
            keys = pg.key.get_pressed()
            for paddle in self.paddles:
                paddle.check_input(keys)
            
            if self.counter_active():
                self.check_counter()

        self.paddles_group.update(dt, self.ball)
        self.ball_group.update(dt, self.paddles)

        self.render_frame(display_surf)