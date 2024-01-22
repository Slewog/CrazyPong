import pygame as pg

from .const.settings import HUD
from .objects.paddle import Paddle
from .objects.ball import Ball

class Level:
    COUNTER_OFFSET_Y = HUD['counter_offset_y']
    COUNT_BG_OFFSET = HUD['counter_bg_offset']
    FONT: pg.font.Font
    FONT_COLOR: pg.Color
    BG_COLOR: pg.Color

    SCREEN_MW: int
    SCREEN_MH: int
    SCREEN_W_QUART: int

    def __init__(self, level_type: str, debug) -> None:
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
        self.reset_time = pg.time.get_ticks()

    def start(self):
        self.started = not self.started
        self.reset_time = pg.time.get_ticks()

    def destroy(self) -> None:
        self.ball.kill()

        for paddle in self.paddles:
            paddle.destroy()
    
    def counter_active(self):
        return self.reset_time != 0
    
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

                if winned:
                    self.winned = winned
                
                self.ball.reset(self.winned)
                break
    
    def update_counter(self, value: int) -> None:
        self.counter = value
        # Create a new counter text surface on update.
        self.counter_txt = self.FONT.render(
            str(self.counter), True, self.FONT_COLOR)
        
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
            self.freeze_time = int(0)
            self.update_counter(-1)

    def render_frame(self, display_surf: pg.Surface) -> None:
        self.paddles_group.draw(display_surf)
        self.ball_group.draw(display_surf)

        if self.winned:
            # Render text to said who win.
            # Render text or button to restart or leave.
            pass

        if self.started and not self.winned and not self.ball.active and self.counter_active():
            pg.draw.rect(display_surf, self.BG_COLOR, self.counter_bg)
            display_surf.blit(self.counter_txt, self.counter_rect)

    def run(self, display_surf: pg.Surface, dt: float) -> None:
        if not self.winned:
            keys = pg.key.get_pressed()
            for paddle in self.paddles:
                paddle.check_input(keys)
            
            if not self.ball.active and self.counter_active():
                self.check_counter()

        self.paddles_group.update(dt, self.ball)
        self.ball_group.update(dt, self.paddles)

        self.render_frame(display_surf)