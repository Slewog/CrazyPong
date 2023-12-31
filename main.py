from sys import exit
import pygame as pg
from time import time

from settings import GameSettings
from locales import Locales
from sprites import Ball, Player
from utils import load_color, load_sound, DebugTools


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
        pg.display.set_caption(Locales.GAME_NAME)

        self.winned = bool(False)
        self.playing = bool(False)

        # sprite group setup
        self.all_sprites = pg.sprite.Group()

    def load_assets(self) -> None:
        # UI.
        self.font = pg.font.Font('freesansbold.ttf', 40)
        self.font_color = load_color(GameSettings.FONT_COLOR)
        self.obj_color = load_color(GameSettings.OBJECT_COLOR)
        self.bg_color = load_color(GameSettings.BACKGROUND_COLOR)
        self.display_surf.fill(self.bg_color)
        pg.display.flip()

        # Middle line.
        self.middle_line_w = GameSettings.MIDDLE_LINE_W
        self.middle_line_clr = load_color(GameSettings.MIDDLE_LINE_COLOR)
        self.middle_line_start = (self.SCREEN_W // 2 - self.middle_line_w//2, int(0))
        self.middle_line_end = (self.SCREEN_W // 2 - self.middle_line_w//2, self.SCREEN_H)
        
        # Texts.
        self.win_txt_pos = (self.SCREEN_W // 2, self.SCREEN_H//2 - 70)
        self.start_txt = self.font.render(Locales.START_TXT, True, self.obj_color)
        self.start_txt_rect = self.start_txt.get_rect(center = (self.SCREEN_W // 2, self.SCREEN_H//2 + 60))
        self.restart_txt = self.font.render(Locales.RESTART_TXT, True, self.obj_color)
        self.restart_txt_rect = self.restart_txt.get_rect(center = (self.SCREEN_W // 2, self.SCREEN_H//2 + 60))

        # Sounds
        hit_sound = load_sound('pong.ogg', GameSettings.HIT_SOUND_VOL)
        score_sound = load_sound('score.ogg', GameSettings.SCORE_SOUND_VOL)

        # Players.
        self.player_left = Player('left', Locales.PLAYER_LEFT, self.SCREEN_W, self.SCREEN_H, self.all_sprites, self.font, self.font_color, self.obj_color)
        self.player_right = Player('right', Locales.PLAYER_RIGHT, self.SCREEN_W, self.SCREEN_H, self.all_sprites, self.font, self.font_color, self.obj_color)
        self.players:list[Player] = [self.player_left, self.player_right]

        # Objects.
        self.ball = Ball(self.SCREEN_W, self.SCREEN_H, self.font, self.font_color, self.obj_color, self.all_sprites, self.player_left, self.player_right, self.MAX_SCORE, [hit_sound, score_sound])

    def quit(self):
        """Kill all sprites and close pygame before quit python"""
        sprites:list[pg.sprite.Sprite] = [self.ball, self.player_left, self.player_right]

        for sprite in sprites:
            sprite.kill()
        
        pg.quit()
        exit()
    
    def reset(self, player_dir:bool) -> None:
        """Reset players direction or all entities"""
        if player_dir:
            for player in self.players:
                player.reset_direction(False)
            return
        
        for player in self.players:
            player.reset()

        self.ball.reset(True)
        self.winned = bool(False)
    
    def start(self) -> None:
        self.playing = bool(True)
        self.ball.set_active(True)

    def render(self) -> None:
        """Draw the frame."""
        # Draw the background.
        self.display_surf.fill(self.bg_color)

        # Draw the middle line.
        pg.draw.line(self.display_surf, self.middle_line_clr, self.middle_line_start, self.middle_line_end, self.middle_line_w)

        self.all_sprites.draw(self.display_surf)

        for player in self.players:
            player.draw_hud(self.display_surf)
        
        if self.winned:
            pg.draw.rect(self.display_surf, self.bg_color, self.win_text_rect)
            self.display_surf.blit(self.win_text, self.win_text_rect)
            pg.draw.rect(self.display_surf, self.bg_color, self.restart_txt_rect)
            self.display_surf.blit(self.restart_txt, self.restart_txt_rect)

        if not self.playing:
            pg.draw.rect(self.display_surf, self.bg_color, self.start_txt_rect)
            self.display_surf.blit(self.start_txt, self.start_txt_rect)

        if self.playing and self.ball.freeze_time != 0:
            self.ball.draw_restart_counter(self.display_surf, self.bg_color)

        if self.playing and self.DEBUG and not self.winned:
            self.debug_tool.render(self.display_surf)

    def run(self) -> None:
        self.load_assets()
        self.prev_dt = time()

        while True:
            """Update the game."""
            # Pygame event loop.
            for event in pg.event.get():
                # Check to close the game.
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.quit()
                
                # Check to reset the game after a player won.
                if self.playing and self.winned and event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    self.reset(False)

                # Check to start the game after launching.
                if not self.playing and event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    self.start()

            dt = time() - self.prev_dt
            self.prev_dt = time()

            self.all_sprites.update(dt)

            if self.playing and not self.winned:
                keys = pg.key.get_pressed()

                for player in self.players:
                    player.check_input(keys)

                    if not self.winned and player.score == self.MAX_SCORE:
                        self.win_text = self.font.render(Locales.WIN_TXT.format(player = player.side_trslt), True, self.font_color)
                        self.win_text_rect = self.win_text.get_rect(center = self.win_txt_pos)
                        self.winned =  bool(True)
                        self.reset(True)

                if not self.ball.active and self.ball.freeze_time != 0:
                    self.ball.check_freeze_time()

                if self.DEBUG:
                    print(self.clock.get_fps())
                    self.debug_tool.add_data(f"- delta : {round(dt, 9)}")
                    self.debug_tool.add_data(f"- player : {round(self.player_right.VELOCITY * dt, 3)}")
                    self.debug_tool.add_data(f"- ball y : {round(self.ball.calcule_speed(self.ball.vel_y, dt), 3)}")
                    self.debug_tool.add_data(f"- ball x : {round(self.ball.calcule_speed(self.ball.vel_x, dt), 3)}")
                    self.debug_tool.add_data(f"- ball dir x : {self.ball.direction.x}")
                    self.debug_tool.add_data(f"- ball dir y : {self.ball.direction.y}")

            self.render()

            """Update the window."""
            pg.display.flip()

            """Frame Cap."""
            if self.USE_FPS:
                self.clock.tick(self.FPS)


if __name__ == '__main__':
    Pong().run()