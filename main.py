import sys
from os import path
import pygame as pg
from time import time

from settings import GameSettings, DebugSettings
from locales import Locales
from sprites import Ball, Player

MAIN_DIR = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))

def resource_path(directory:str, resource:str) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    return path.join(MAIN_DIR, directory, resource)


class NoneSound:
    def play(self):
        pass


def load_sound(sound:str, vol:float=1.0):
    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()
    
    try:
        loaded_sound = pg.mixer.Sound(resource_path("assets/sounds", sound))
    except FileNotFoundError:
        return NoneSound()
    
    loaded_sound.set_volume(vol)
    return loaded_sound

class DebugTools:
    def __init__(self) -> None:
        self.data:list[str] = []
        self.font = pg.font.Font(None, DebugSettings.FONT_SIZE)
        self.border_radius = DebugSettings.BORDER_RADIUS

        self.rect = pg.Rect(DebugSettings.X_POS, DebugSettings.Y_POS, DebugSettings.WIDTH, DebugSettings.HEIGHT)

        self.font.set_underline(True)
        self.font.set_bold(True)
        self.font.set_italic(True)
        self.title = self.font.render('DEBUG TOOLS:', True, 'white')
        self.title_rect = self.title.get_rect(midtop = (self.rect.midtop[0], self.rect.midtop[1] + 10))
        self.font.set_underline(False)
        self.font.set_bold(False)

        self.offset = self.title_rect.bottom + 10

    def add_data(self, data:str):
        self.data.append(data)
    
    def render(self, display:pg.Surface):
        pg.draw.rect(display, 'Black', self.rect, border_radius=self.border_radius)
        display.blit(self.title, self.title_rect)

        offset = self.offset

        for data in self.data:
            data_txt = self.font.render(data, True, 'white')

            data_txt_rect = data_txt.get_rect(topleft = (self.rect.left + 10, offset))
            display.blit(data_txt, data_txt_rect)
            offset += data_txt_rect.height + 5
        
        self.data:list[str] = []

class Pong:
    FPS = GameSettings.FPS
    USE_FPS = GameSettings.USE_FPS
    SCREEN_H = GameSettings.SCREEN_H
    SCREEN_W = GameSettings.SCREEN_W
    MAX_SCORE = GameSettings.MAX_SCORE
    DEBUG = GameSettings.DEBUG

    def __init__(self) -> None:
        # Setup.
        pg.mixer.pre_init(44100, -16, 2, 512)
        pg.init()

        self.debug_tool = DebugTools()

        self.clock = pg.time.Clock()
        
        self.display_surf = pg.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        pg.display.set_caption(Locales.game_name)

        self.winned = False
        self.playing = False

        # sprite group setup
        self.all_sprites = pg.sprite.Group()

    def load_assets(self) -> None:
        # UI.
        self.font = pg.font.SysFont('comicsans', 50)

        if type(GameSettings.FONT_COLOR) == tuple:
            self.font_color = GameSettings.FONT_COLOR
        else:
            self.font_color = pg.Color(GameSettings.FONT_COLOR)

        if type(GameSettings.OBJECT_COLOR) == tuple:
            self.obj_color = GameSettings.OBJECT_COLOR
        else:
            self.obj_color = pg.Color(GameSettings.OBJECT_COLOR)

        self.bg_color = pg.Color(GameSettings.BACKGROUND_COLOR)
        self.display_surf.fill(self.bg_color)
        pg.display.flip()

        # Text.
        self.win_txt_pos = (self.SCREEN_W // 2, self.SCREEN_H//2 - 70)

        self.start_txt = self.font.render(Locales.START_TXT, True, self.obj_color)
        self.start_txt_rect = self.start_txt.get_rect(center = (self.SCREEN_W // 2, self.SCREEN_H//2 + 60))
        
        self.restart_txt = self.font.render(Locales.RESTART_TXT, True, self.obj_color)
        self.restart_txt_rect = self.restart_txt.get_rect(center = (self.SCREEN_W // 2, self.SCREEN_H//2 + 60))

        # Players.
        self.player_left = Player('left', Locales.PLAYER_LEFT, self.SCREEN_W, self.SCREEN_H, self.all_sprites, self.font, self.font_color, self.obj_color)
        self.player_right = Player('right', Locales.PLAYER_RIGHT, self.SCREEN_W, self.SCREEN_H, self.all_sprites, self.font, self.font_color, self.obj_color)
        self.players:list[Player] = [self.player_left, self.player_right]

        # Sounds
        hit_sound = load_sound('pong.ogg', GameSettings.HIT_SOUND_VOL)
        score_sound = load_sound('score.ogg', GameSettings.SCORE_SOUND_VOL)

        # Objects.
        self.ball = Ball(self.SCREEN_W, self.SCREEN_H, self.obj_color, self.all_sprites, self.player_left, self.player_right, [hit_sound, score_sound])

    def quit(self):
        sprites:list[pg.sprite.Sprite] = [self.ball, self.player_left, self.player_right]

        for sprite in sprites:
            sprite.kill()
        
        pg.quit()
        sys.exit()
    
    def reset(self) -> None:
        if self.winned:
            for player in self.players:
                player.reset()

            self.ball.reset(True)
            
            self.winned = False

    def render(self) -> None:
        # Draw the background.
        self.display_surf.fill(self.bg_color)

        self.all_sprites.draw(self.display_surf)

        for player in self.players:
            player.draw_hud(self.display_surf)
        
        if self.winned:
            self.display_surf.blit(self.win_text, self.win_text_rect)
            self.display_surf.blit(self.restart_txt, self.restart_txt_rect)

        if not self.playing:
            self.display_surf.blit(self.start_txt, self.start_txt_rect)

        if self.playing and self.DEBUG and not self.winned:
            self.debug_tool.render(self.display_surf)

        # Update the window.
        pg.display.flip()

    def run(self) -> None:
        self.load_assets()
        self.prev_dt = time()

        while True:
            ### Event loop. ###
            for event in pg.event.get():
                # Check to close the game.
                if event.type == pg.QUIT:
                    self.quit()
                
                # Check to reset the game after a player won.
                if self.winned and event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    for player in self.players:
                        player.reset()
                    self.ball.reset(True)
                    self.winned = False

                # Check to start the game after launching.
                if not self.playing and event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    self.playing = True

            ### Update the game. ###
            self.dt = time() - self.prev_dt
            self.prev_dt = time()

            if self.playing and not self.winned:
                keys = pg.key.get_pressed()

                for player in self.players:
                    player.check_input(keys)

                    if not self.winned and player.score == self.MAX_SCORE:
                        self.win_text = self.font.render(Locales.WIN_TXT.format(player = player.side_trslt), True, self.font_color)
                        self.win_text_rect = self.win_text.get_rect(center = self.win_txt_pos)
                        self.winned = True

                self.all_sprites.update(self.dt)

                if self.DEBUG:
                    self.debug_tool.add_data(f"- player : {round(self.player_right.VELOCITY * self.dt, 3)}")
                    self.debug_tool.add_data(f"- ball y : {round(self.ball.calcule_speed(self.ball.vel_y, self.dt), 3)}")
                    self.debug_tool.add_data(f"- ball x : {round(self.ball.calcule_speed(self.ball.vel_x, self.dt), 3)}")
                    self.debug_tool.add_data(f"- ball dir x : {self.ball.direction.x}")
                    self.debug_tool.add_data(f"- ball dir y : {self.ball.direction.y}")

            ### Draw the frame. ###
            self.render()

            ### Apply frame cap. ###
            if self.USE_FPS:
                self.clock.tick(self.FPS)


if __name__ == '__main__':
    Pong().run()