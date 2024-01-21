import pygame as pg
from sys import exit
from time import time
from typing import Dict

from .const.custom_typing import SoundData
from .const.custom_event import CE_BTN_CLICKED
from .const.settings import GAME, FONT, COLORS, CRS_EFFECT, SOUNDS
from .utils import load_color, load_img, load_sound

from .debug import DebugTool

from .ui.screen_effect import CRS
from .ui.starting_menu import StartingMenu
from .objects.paddle import Paddle
from .objects.ball import Ball


class Level:
    def __init__(self, level_type: str) -> None:
        self.ball_group = pg.sprite.GroupSingle()
        self.paddles_group = pg.sprite.Group()

        self.winned = bool(False)

        if level_type == 'oneplayer':
            self.paddle_left = Paddle('left', 'player', self.paddles_group)
            self.paddle_right = Paddle('right', 'ai', self.paddles_group)
        else:
            self.paddle_left = Paddle('left', 'player', self.paddles_group)
            self.paddle_right = Paddle('right', 'player', self.paddles_group)

        self.ball = Ball(self.ball_group)

        self.paddles = [self.paddle_left, self.paddle_right]

    def destroy(self):
        self.ball.kill()

        for paddle in self.paddles:
            paddle.kill()
    
    def render_frame(self, display_surf: pg.Surface):
        self.paddles_group.draw(display_surf)
        self.ball_group.draw(display_surf)

    def run(self, display_surf: pg.Surface, dt: float):
        if not self.winned:
            keys = pg.key.get_pressed()
            for paddle in self.paddles:
                paddle.check_input(keys)

        self.paddles_group.update(dt, self.ball)
        self.ball_group.update(dt, self.paddles)

        self.render_frame(display_surf)
        

class Pong:
    FPS = GAME['fps']
    SCREEN_RECT = pg.Rect(0, 0, GAME['width'], GAME['height'])
    SCREEN_MW = SCREEN_RECT.width // 2
    SCREEN_MH = SCREEN_RECT.height // 2

    crs_effect: CRS
    level:Level = None
    starting_menu: StartingMenu
    colors: Dict[str, pg.Color] = {}

    def __init__(self) -> None:
        pg.mixer.pre_init(44100, -16, 2, 512)
        pg.init()

        self.clock = pg.time.Clock()

        self.display_surf = pg.display.set_mode((self.SCREEN_RECT.size))
        pg.display.set_caption(GAME['name'])

        self.debug = DebugTool(self.display_surf)
        self.state = str('menu')

    def load(self) -> None:
        for color_name, color in COLORS.items():
            self.colors[color_name] = load_color(color)

        CRS_EFFECT['vignette'] = load_img(CRS_EFFECT['file'], convert_a=True)
        CRS_EFFECT['line_color'] = load_color(CRS_EFFECT['line_color'])
        CRS_EFFECT['screen_rect'] = self.SCREEN_RECT

        self.crs_effect = CRS(CRS_EFFECT)
        self.starting_menu = StartingMenu(FONT, self.colors['font'], self.colors['background'])
        self.middle_rect = pg.Rect(
            self.SCREEN_MW - GAME['middle_rect_w'] // 2,
            int(0),
            GAME['middle_rect_w'],
            self.SCREEN_RECT.height
        )

        self.display_surf.fill(self.colors['background'])
        pg.draw.rect(self.display_surf, self.colors['font'], self.middle_rect)
        self.starting_menu.render(self.display_surf)
        pg.display.flip()

        ball_sound_data:SoundData = SOUNDS['ball']
        Ball.SCREEN_RECT = self.SCREEN_RECT
        Ball.START_POS = (self.SCREEN_MW, self.SCREEN_MH)
        Ball.COLOR = self.colors['objects']
        Ball.HIT_SOUND = load_sound(ball_sound_data['file'], vol=ball_sound_data['vol'])

        Paddle.SCREEN_RECT = self.SCREEN_RECT
        Paddle.SCREEN_CENTERY = self.SCREEN_MH
        Paddle.SCREEN_BOTTOM = self.SCREEN_RECT.height - Paddle.OFFSET_Y
        Paddle.COLOR = self.colors['objects']
    
    def set_state(self, new_state: str) -> None:
        if self.state == new_state or type(new_state) != str:
            return
        
        if new_state == 'quit':
            self.quit()
        
        self.state = new_state

    def select_game_type(self, type_target: str) -> None:
        self.level = Level(type_target)
        self.set_state('play')

    def quit_current_game(self) -> None:
        self.starting_menu.buttons[0].CLICK_SOUND.play()

        self.level.destroy()
        self.set_state('menu')
        self.level = None

    def quit(self) -> None:
        pg.display.quit()
        pg.quit()
        exit()

    def run(self) -> None:
        self.load()
        prev_dt = time()

        while True:
            self.clock.tick(self.FPS)

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.set_state('quit')
                
                if self.level is not None and e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    self.quit_current_game()
                    
                if self.state == 'menu' and e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                    self.starting_menu.handle_btn_click()
                
                if e.type == CE_BTN_CLICKED:
                    if e.action == 'quit':
                        self.set_state('quit')
                    elif e.action == 'play' and self.level is None:
                        self.select_game_type(e.target_level)

            current_time = time()
            dt = current_time - prev_dt
            prev_dt = current_time

            self.display_surf.fill(self.colors['background'])
            pg.draw.rect(self.display_surf, self.colors['font'], self.middle_rect)

            if self.state == 'menu':
                self.starting_menu.render(self.display_surf)

            if self.state == 'play' and self.level is not None:
                self.level.run(self.display_surf, dt)

            self.crs_effect.render(self.display_surf)

            pg.display.flip()