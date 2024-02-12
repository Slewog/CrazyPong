from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entities import Ball

from pygame import Surface, sprite, time, mouse, draw, key
from pygame.font import Font
from pygame.mixer import Sound

from src.const.custom_typing import CollisionValue
from src.const.settings import SCREEN_RECT, FONT_CLR, BG_CLR, HUD
from src.ui.button import ButtonList
from .utils import Text
from src.entities import Paddle


class Level:
    WIN_TXT_POS = (
        SCREEN_RECT.centerx,
        SCREEN_RECT.height // 2 - HUD['winner_msg_offset']
    )

    COUNTER_POS = (SCREEN_RECT.centerx, HUD['counter_pos_y'])
    COUNT_BG_OFFSET = HUD['counter_bg_offset']
    SCREEN_W_QUART = SCREEN_RECT.centerx // 2
    FONT_COLOR = FONT_CLR
    BG_COLOR = BG_CLR

    TXT_FONT: Font
    COUNTER_FONT: Font
    SCORE_SOUND: Sound
    WIN_SOUND: Sound
    BUTTONS: ButtonList

    def __init__(self, level_type: str, ball: Ball, ball_grp: sprite.GroupSingle) -> None:
        self.paddles_grp = sprite.Group()
        self.ball_grp = ball_grp

        self.winned = bool(False)
        self.started = bool(False)
        self.counter = int(-1)
        self.reset_time = int(0)

        self.ball = ball
        self.paddles = [
            Paddle('left', 'player', self.SCREEN_W_QUART, self.paddles_grp),
            Paddle('right', 'ai' if level_type == 'oneplayer' else 'player', self.SCREEN_W_QUART * 3, self.paddles_grp)
        ]

    def reset(self) -> None:
        for paddle in self.paddles:
            paddle.reset()

        self.winned = bool(False)

        self.reset_time = time.get_ticks()

        self.ball.reset(True)

    def start(self) -> None:
        self.started = not self.started
        self.reset_time = time.get_ticks()

    def destroy(self) -> None:
        self.ball.reset(True)

        for paddle in self.paddles:
            paddle.destroy()

    def handle_btn_click(self) -> None:
        for button in self.BUTTONS:
            if button.hovered:
                button.click()
                break

    def counter_active(self) -> bool:
        return self.reset_time != 0
    
    def update_counter(self, value: int) -> None:
        self.counter = value

        self.counter_txt = self.COUNTER_FONT.render(str(self.counter), True, self.FONT_COLOR)
        self.counter_rect = self.counter_txt.get_rect(midbottom=self.COUNTER_POS)

        self.counter_bg = self.counter_rect.copy()
        self.counter_bg.move_ip(0, -self.COUNT_BG_OFFSET)

    def check_counter(self) -> None:
        reset_time = time.get_ticks() - self.reset_time

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

    def add_point_to_paddle(self, target: str) -> None:
        """target is the side of the paddle targetted"""
        if type(target) != str: return

        for paddle in self.paddles:
            if paddle.side == target:
                paddle.score.add_point()
                winned = paddle.winned()

                if not winned:
                    self.reset_time = time.get_ticks()
                    self.SCORE_SOUND.play()

                if winned:
                    self.winned = winned
                    self.win_text = Text(
                        self.TXT_FONT,
                        "The AI is the winner" if paddle.type == 'ai' else f"The player {paddle.side} is the winner",
                        self.WIN_TXT_POS,
                        'center',
                        bg=True,
                        bg_offset_y= 3
                    )

                    self.WIN_SOUND.play()
                
                self.ball.reset(self.winned)
                break

    def intercept_collision(self, dist_x: int, dist_y: int, ball: 'Ball', paddle: Paddle) -> CollisionValue:
        abs_distx = abs(dist_x) # abs(self.ball.rect.centerx - paddle.rect.centerx)
        abs_disty = abs(dist_y) # abs(self.ball.rect.centery - paddle.rect.centery)
        
        # Too far of x or y axis to collide.
        if abs_distx > paddle.H_WIDTH + ball.RADIUS or abs_disty > paddle.H_HEIGHT + ball.RADIUS:
            return False, None, None
        
        # Vertical Collision.
        if abs_distx <= paddle.H_WIDTH:
            return True, None, 'top' if dist_y < 0 else 'bottom'
        
        # Horizontal Collision.
        if abs_disty <= paddle.H_HEIGHT:
            return True, None, 'left' if dist_x < 0 else 'right'
        
        # Corner Collision.
        corner_dist_sq = (abs_distx - paddle.H_WIDTH) ** 2 + (abs_disty - paddle.H_HEIGHT) ** 2
        if corner_dist_sq <= ball.RADIUS_SQ:
            if ball.rect.centerx < paddle.rect.centerx:
                return True, 'topleft' if ball.rect.centery < paddle.rect.centery else 'bottomleft', None
            else:
                return True, 'topright' if ball.rect.centery < paddle.rect.centery else 'bottomright', None

        return False, None, None
    
    def render_frame(self, display_surf: Surface) -> None:
        self.paddles_grp.draw(display_surf)

        if self.winned:
            display_surf.blit(self.win_text.surf, self.win_text.rect)
            mouse_pos = mouse.get_pos()
            for button in self.BUTTONS:
                button.render(display_surf, mouse_pos)
            return
        
        if self.counter_active():
            draw.rect(display_surf, self.BG_COLOR, self.counter_bg)
            self.ball_grp.draw(display_surf)
            display_surf.blit(self.counter_txt, self.counter_rect)
            return
        
        self.ball_grp.draw(display_surf)

    def run(self, display_surf: Surface, dt: float) -> None:
        if not self.winned:
            if self.counter_active():
                self.check_counter()
        
        keys = key.get_pressed()
        self.paddles_grp.update(dt, keys, self.ball)

        if self.ball.active:
            self.ball.update(dt)

            if self.ball.pos.x < SCREEN_RECT.centerx:
                paddle = self.paddles[0]
            else:
                paddle = self.paddles[1]

            dist_x = self.ball.rect.centerx - paddle.rect.centerx
            dist_y = self.ball.rect.centery - paddle.rect.centery

            collision, corner, side = self.intercept_collision(dist_x, dist_y, self.ball, paddle)
            if collision:
                self.ball.paddle_collision(side, corner, dist_x, dist_y, paddle)

        self.render_frame(display_surf)