import pygame as pg
from sys import exit
from time import time

from .const.custom_event import CE_BTN_CLICKED
from .const.settings import GAME, FONT, COLORS
from .utils import load_color

from .debug import DebugTool

from .ui.menu import Menu
from .objects.paddle import Paddle
from .objects.ball import Ball


class GameType:
    def __init__(self, game_type: str, ball_group: pg.sprite.GroupSingle(), paddles_group: pg.sprite.Group(), all: pg.sprite.Group()) -> None:
        if game_type == 'oneplayer':
            self.paddle_left = Paddle('left', 'player', paddles_group, all)
            self.paddle_right = Paddle('right', 'ai', paddles_group, all)
        else:
            self.paddle_left = Paddle('left', 'player', paddles_group, all)
            self.paddle_right = Paddle('right', 'player', paddles_group, all)

        self.ball = Ball(self.paddle_left, self.paddle_right, ball_group, all)


class Pong:
    FPS = GAME['fps']
    SCREEN_RECT = pg.Rect(0, 0, GAME['width'], GAME['height'])
    SCREEN_MW = SCREEN_RECT.width // 2
    SCREEN_MH = SCREEN_RECT.height // 2

    def __init__(self) -> None:
        pg.mixer.pre_init(44100, -16, 2, 512)
        pg.init()

        self.clock = pg.time.Clock()

        self.display_surf = pg.display.set_mode((self.SCREEN_RECT.size))
        pg.display.set_caption(GAME['name'])

        self.debug = DebugTool(self.display_surf)

        self.ball_group = pg.sprite.GroupSingle()
        self.paddle_group = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.current_game = None
        self.state = str('menu')
        self.colors: dict[str, pg.Color] = {}

    def set_state(self, new_state: str):
        if self.state == new_state or type(new_state) != str:
            return
        
        if new_state == 'quit':
            self.quit()
        
        self.state = new_state

    def load(self):
        for color_name, color in COLORS.items():
            self.colors[color_name] = load_color(color)

        self.menu = Menu(FONT, self.colors['font'], self.colors['background'])

        self.display_surf.fill(self.colors['background'])
        self.middle_rect = pg.Rect(
            self.SCREEN_MW - GAME['middle_rect_w']//2,
            int(0),
            GAME['middle_rect_w'],
            self.SCREEN_RECT.height
        )
        pg.draw.rect(self.display_surf, self.colors['font'], self.middle_rect)
        pg.display.flip()

        Ball.SCREEN_RECT = self.SCREEN_RECT
        Ball.START_POS = (self.SCREEN_MW, self.SCREEN_MH)
        Ball.COLOR = self.colors['objects']

        Paddle.SCREEN_RECT = self.SCREEN_RECT
        Paddle.SCREEN_CENTERY = self.SCREEN_MH
        Paddle.SCREEN_BOTTOM = self.SCREEN_RECT.height - Paddle.OFFSET_Y
        Paddle.COLOR = self.colors['objects']

    def select_game_type(self, type_target: str):
        self.current_game = GameType(type_target, self.ball_group, self.paddle_group, self.all_sprites)
        self.set_state('play')

    def quit_current_game(self):
        for sprite in self.all_sprites:
            sprite: pg.sprite.Sprite
            sprite.kill()

        self.set_state('menu')
        self.current_game = None

    def quit(self):
        pg.quit()
        exit()

    def render_frame(self):
        pass

    def run(self):
        self.load()
        prev_dt = time()

        while True:
            self.clock.tick(self.FPS)

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.set_state('quit')
                
                if self.current_game is not None and e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    self.quit_current_game()
                    
                if self.state == 'menu' and e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                    self.menu.handle_btn_click()
                
                if e.type == CE_BTN_CLICKED:
                    if e.action == 'quit':
                        self.set_state('quit')
                    elif e.action == 'play' and self.current_game is None:
                        self.select_game_type(e.target_level)

            current_time = time()
            dt = current_time - prev_dt
            prev_dt = current_time

            self.display_surf.fill(self.colors['background'])
            pg.draw.rect(self.display_surf, self.colors['font'], self.middle_rect)

            if self.state == 'menu':
                self.menu.render(self.display_surf)

            if self.state == 'play':
                self.all_sprites.draw(self.display_surf)

                keys = pg.key.get_pressed()
                self.paddle_group.update(dt, keys, self.current_game.ball)
                self.ball_group.update(dt)

            pg.display.flip()