import sys
import pygame as pg
from time import time

from settings import GameSettings
from locales import Locales
from sprites import Ball, Player


class Pong:
    FPS = GameSettings.FPS
    USE_FPS = GameSettings.USE_FPS
    SCREEN_H = GameSettings.SCREEN_H
    SCREEN_W = GameSettings.SCREEN_W
    MAX_SCORE = GameSettings.MAX_SCORE

    def __init__(self) -> None:
        # Setup.
        # pg.mixer.pre_init(22050, -16, 2, 1024)
        pg.init()

        self.clock = pg.time.Clock()
        self.display_surf = pg.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        pg.display.set_caption(Locales.game_name)

        # sprite group setup
        self.all_sprites = pg.sprite.Group()

        # Objects and Player.
        self.player_left = Player('left', self.SCREEN_W, self.SCREEN_H, self.all_sprites)
        self.player_right = Player('right', self.SCREEN_W, self.SCREEN_H, self.all_sprites)
        self.ball = Ball(self.SCREEN_W, self.SCREEN_H, self.all_sprites, self.player_left, self.player_right)

    def load_assets(self) -> None:
        pass

    def quit(self):
        sprites:list[pg.sprite.Sprite] = [self.ball, self.player_left, self.player_right]
        
        for sprite in sprites:
            sprite.kill()
        
        pg.quit()
        sys.exit()

    def update(self) -> None:
        # Delta time.
        self.dt = time() - self.prev_dt
        self.prev_dt = time()

        self.all_sprites.update(self.dt)

    def render(self) -> None:
        # Draw the background.
        self.display_surf.fill('cyan')

        self.all_sprites.draw(self.display_surf)

        # Update the window.
        pg.display.update()
        # pg.display.flip()

    def run(self) -> None:
        self.load_assets()
        self.prev_dt = time()

        while True:
            # Event loop.
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()

            # Update the game.
            self.update()

            # Draw the frame.
            self.render()

            # Apply frame cap.
            if self.USE_FPS:
                self.clock.tick(self.FPS)


if __name__ == '__main__':
    Pong().run()