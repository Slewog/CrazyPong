import pygame as pg
from sys import exit
from time import time
from typing import Dict

from .const.custom_typing import SoundData
from .const.custom_event import CE_BTN_CLICKED, CE_BALL_OUT_SCREEN
from .const.settings import GAME, FONT, COLORS, CRS_EFFECT, SOUNDS, BUTTON_ANIMATE
from .utils import load_color, load_img, load_sound, load_font, Text, RectBackground

from .debug import DebugTool

from .ui.screen_effect import CRS
from .ui.buttons import ButtonAnimate
from .ui.starting_menu import StartingMenu
from .level import Level
from .objects.paddle import Paddle
from .objects.ball import Ball


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
        # UI loading.
        for color_name, color in COLORS.items():
            self.colors[color_name] = load_color(color)

        CRS_EFFECT['vignette'] = load_img(CRS_EFFECT['file'], convert_a=True)
        CRS_EFFECT['line_color'] = load_color(CRS_EFFECT['line_color'])
        CRS_EFFECT['screen_rect'] = self.SCREEN_RECT

        self.crs_effect = CRS(CRS_EFFECT)

        Text.COLOR = self.colors['font']
        RectBackground.COLOR = self.colors['background']

        ButtonAnimate.FONT = load_font(FONT['family'], FONT['default_size'])
        ButtonAnimate.FONT_COLOR = self.colors['font']
        ButtonAnimate.CLICK_SOUND = load_sound(BUTTON_ANIMATE['sound_file'], BUTTON_ANIMATE['sound_vol'])

        self.starting_menu = StartingMenu(FONT)
        self.middle_rect = pg.Rect(
            self.SCREEN_MW - GAME['middle_rect_w'] // 2,
            0,
            GAME['middle_rect_w'],
            self.SCREEN_RECT.height
        )

        self.display_surf.fill(self.colors['background'])
        pg.draw.rect(self.display_surf, self.colors['font'], self.middle_rect)
        self.starting_menu.render(self.display_surf)
        pg.display.flip()

        # level and objects.
        Level.FONT = load_font(FONT['family'], FONT['hud_size'])
        Level.FONT_COLOR = self.colors['font']
        Level.BG_COLOR = self.colors['background']
        Level.SCREEN_MW = self.SCREEN_MW
        Level.SCREEN_MH = self.SCREEN_MH
        Level.SCREEN_W_QUART = self.SCREEN_MW // 2
        Level.COUNT_BG_OFFSET = GAME['hud']['counter_bg_offset']
        Level.COUNTER_OFFSET_Y = GAME['hud']['counter_offset_y']
        Level.SCORE_OFFSET_Y = GAME['hud']['score_offset_y']

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
        self.level = Level(type_target, self.debug.add_data)
        self.set_state('play')
        self.level.start()

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
                
                if self.level is not None:
                    if e.type == CE_BALL_OUT_SCREEN:
                        self.level.add_point_to_paddle(e.target)

                    if e.type == pg.KEYDOWN:
                        if e.key == pg.K_ESCAPE or e.key == pg.K_BACKSPACE:
                            self.quit_current_game()
                            break

                        if self.level.winned and e.key == pg.K_SPACE:
                            self.level.reset()
                        
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