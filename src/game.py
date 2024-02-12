import pygame as pg
from pygame.locals import QUIT, MOUSEBUTTONDOWN, K_ESCAPE, K_BACKSPACE

from time import time
from sys import exit

from src.const.settings import *

pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()
pg.mixer.set_num_channels(64)
pg.display.set_caption(GAME_NAME)

from src.entities import Ball, Score
from src.utils import load_font, load_img, load_sound
from src.ui.menu import StartingMenu
from .ui.screen_effect import CRS
from src.level import Level


class CrazyPong():
    FPS = FPS
    
    crs_effect: CRS
    background: pg.Surface
    starting_menu: StartingMenu
    level:Level = None

    def __init__(self) -> None:

        self.clock = pg.time.Clock()
        self.display_surf = pg.display.set_mode(SCREEN_RECT.size)

        self.paddles_grp = pg.sprite.Group()
        self.ball_grp = pg.sprite.GroupSingle()

        self.state = str('menu')

    def create_background(self):
        tmp_surf = pg.Surface(self.display_surf.get_size())
        tmp_surf.fill(BG_CLR)

        pg.draw.rect(tmp_surf, FONT_CLR, (
            SCREEN_RECT.centerx - MIDDLE_LINE_W // 2,
            0,
            MIDDLE_LINE_W,
            SCREEN_RECT.height
        ))
        return tmp_surf.copy()
    
    def load(self):
        self.background = self.create_background()
        pg.display.flip()

        fonts = {}
        for name, size in FONT['sizes'].items():
            fonts[name] = load_font(FONT['family'], size)

        sounds = {}
        for sound, data in SOUNDS.items():
            sounds[sound] = load_sound(data['file'], data['vol'])

        self.crs_effect = CRS(load_img(CRS_EFFECT['file'], convert_a=True))

        from src.ui.button import ButtonAnimate
        ButtonAnimate.FONT = fonts['default']
        ButtonAnimate.CLICK_SOUND = sounds['button']

        Level.TXT_FONT = fonts['win_msg']
        Level.COUNTER_FONT = fonts['counter']
        Level.BUTTONS = [ButtonAnimate(button[0], button[1]) for button in HUD['buttons']]
        Level.SCORE_SOUND = sounds['score']
        Level.WIN_SOUND = sounds['win']
        del ButtonAnimate

        Score.FONT = fonts['score']

        self.starting_menu = StartingMenu(fonts)

        Ball.HIT_SOUND = sounds['ball']
        self.ball = Ball(self.ball_grp)
    
    def set_state(self, new_state: str) -> None:
        if self.state == new_state or type(new_state) != str:
            return
        
        self.state = new_state
        
        if new_state == 'quit':
            self.quit()
    
    def set_game_type(self, type_target: str) -> None:
        self.level = Level(type_target, self.ball, self.ball_grp)
        self.set_state('play')
        self.reset_mouse_cursor()
        self.level.start()
    
    def reset_mouse_cursor(self):
        if pg.mouse.get_cursor()[0] == pg.SYSTEM_CURSOR_HAND:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

    def quit_current_game(self, play_sound: bool) -> None:
        if play_sound:
            self.starting_menu.buttons[0].CLICK_SOUND.play()

        self.level.destroy()
        self.set_state('menu')
        self.level = None

    def quit(self) -> None:
        pg.mixer.stop()
        pg.mixer.quit()

        pg.display.quit()
        pg.quit()
        exit()
    
    def run(self) -> None:
        self.load()
        last_dt = time()

        while True:
            current_time = time()
            dt = current_time - last_dt
            last_dt = current_time

            # Event loop.
            for e in pg.event.get():
                if e.type == QUIT:
                    self.set_state('quit')

                if self.level is not None:
                    if e.type == BALL_OUT_SCREEN:
                        self.level.add_point_to_paddle(e.target)
                    
                    if self.level.winned and e.type == MOUSEBUTTONDOWN and e.button == 1:
                        self.level.handle_btn_click()

                    if e.type == pg.KEYDOWN and (e.key == K_ESCAPE or e.key == K_BACKSPACE):
                        self.quit_current_game(True)
                        break

                if self.state == 'menu' and e.type == MOUSEBUTTONDOWN and e.button == 1:
                    self.starting_menu.handle_btn_click()

                if e.type == BTN_CLICKED:
                    match e.action:
                        case 'quit':
                            self.set_state('quit')
                        case 'play':
                            self.set_game_type(e.target_level)
                        case 'restart':
                            self.level.reset()
                            self.reset_mouse_cursor()
                        case 'backmenu':
                            self.quit_current_game(False)
                            self.reset_mouse_cursor()
                    
            self.display_surf.blit(self.background, (0, 0))

            if self.state == 'menu':
                self.starting_menu.render(self.display_surf)
            elif self.state == 'play':
                self.level.run(self.display_surf, dt)

            self.crs_effect.render(self.display_surf)

            pg.display.flip()
            self.clock.tick(self.FPS)
