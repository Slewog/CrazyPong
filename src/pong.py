import pygame as pg
from sys import exit
from time import time

from .const.custom_event import CE_BTN_CLICKED
from .const.settings import GAME, FONT, COLORS
from .ui.menu import Menu

from .utils import load_color, ColorValue

from .debug import DebugTool

from .objects.ball import Ball
from .objects.paddle import Paddle, PlayerPaddle, AIPaddle

class OnePlayer:
    def __init__(self, screen_centery, ball_group: pg.sprite.GroupSingle(), paddles_group: pg.sprite.Group()) -> None:
        self.left_player = PlayerPaddle('left', screen_centery, paddles_group)
        self.right_player = AIPaddle('right', screen_centery, paddles_group)

        self.ball = Ball(self.left_player, self.right_player, ball_group)

    def update(self, dt, keys: pg.key.ScancodeWrapper):
        self.left_player.update(dt, keys)
        self.right_player.update(dt, self.ball)
        self.ball.update(dt)

class TwoPlayer:
    def __init__(self, screen_centery, ball_group: pg.sprite.GroupSingle(), paddles_group: pg.sprite.Group()) -> None:
    
        self.left_player = PlayerPaddle('left', screen_centery, paddles_group)
        self.right_player = PlayerPaddle('right', screen_centery, paddles_group)

        self.ball = Ball(self.left_player, self.right_player, ball_group)
        
    def update(self, dt, keys: pg.key.ScancodeWrapper):
        self.left_player.update(dt, keys)
        self.right_player.update(dt, keys)
        self.ball.update(dt)

class LevelManager:
    def __init__(self, screen_rect: pg.Rect, screen_centerx: int, screen_centery: int, obj_color, set_game_state) -> None:
        self.set_game_state = set_game_state
        self.screen_centery = screen_centery
        self.current_level = None

        self.ball_group = pg.sprite.GroupSingle()
        self.paddle_group = pg.sprite.Group()

        Ball.SCREEN_RECT = screen_rect
        Ball.START_POS = (screen_centerx, screen_centery)
        Ball.COLOR = obj_color

        Paddle.SCREEN_RECT = screen_rect
        Paddle.SCREEN_CENTERY = screen_centery
        Paddle.SCREEN_BOTTOM = screen_rect.height - Paddle.WALL_OFFSET
        Paddle.COLOR = obj_color

    def select_level(self, target_level):
        if target_level == 'oneplayer':
            self.current_level = OnePlayer(self.screen_centery, self.ball_group, self.paddle_group)
        elif target_level == 'twoplayer':
            self.current_level = TwoPlayer(self.screen_centery, self.ball_group, self.paddle_group)
        
    def quit_level(self):
        self.set_game_state('menu')

        self.paddle_group.empty()
        self.ball_group.empty()
        self.current_level = None

    def update_current_level(self, dt):
        keys = pg.key.get_pressed()
        self.current_level.update(dt, keys)
        
    def render(self, display_surf: pg.Surface):
        self.ball_group.draw(display_surf)
        self.paddle_group.draw(display_surf)


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

        self.menu = Menu()
        self.debug = DebugTool(self.display_surf)

        self.state = str('menu')
        self.colors: dict[str, ColorValue] = {}

    def set_state(self, new_state: str):
        if self.state == new_state or type(new_state) != str:
            return
        
        if new_state == 'quit':
            self.quit()
        
        self.state = new_state

    def load_assets(self):
        for color_name, color in COLORS.items():
            self.colors[color_name] = load_color(color)

        self.menu.load(FONT, self.colors['font'])

        self.display_surf.fill(self.colors['background'])
        pg.display.flip()

        self.level_manager = LevelManager(self.SCREEN_RECT, self.SCREEN_MW, self.SCREEN_MH, self.colors['objects'], self.set_state)

    def quit(self):
        pg.quit()
        exit()

    def run(self):
        self.load_assets()
        prev_dt = time()

        while True:
            self.clock.tick(self.FPS)

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.set_state('quit')
                
                if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    self.level_manager.quit_level()

                if self.state == 'menu' and e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                    self.menu.handle_btn_click()
                
                if e.type == CE_BTN_CLICKED:
                    if e.target_level is not None:
                        self.level_manager.select_level(e.target_level)
                    self.set_state(e.action)

            current_time = time()
            dt = current_time - prev_dt
            prev_dt = current_time

            self.debug.add_data(f"{dt}")

            self.display_surf.fill(self.colors['background'])

            if self.state == 'menu':
                self.menu.render(self.display_surf)

            if self.state == 'play':
                self.level_manager.render(self.display_surf)
                self.level_manager.update_current_level(dt)
            
            # self.debug.render()

            pg.display.flip()