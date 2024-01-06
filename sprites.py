import pygame as pg
from random import choice

from settings import BallSettings, PlayerSettings


class Player(pg.sprite.Sprite):
    VELOCITY = PlayerSettings.VELOCITY
    WALL_OFFSET = PlayerSettings.WALL_OFFSET
    SCORE_Y_POS = PlayerSettings.SCORE_Y_POS

    def __init__(self, side: str, side_trslt: str, screen_w: int, screen_h: int, screen_mh: int, group: pg.sprite.Group, font: pg.font.Font, font_color: pg.Color, color: pg.Color) -> None:
        super().__init__(group)

        # Screen info for collisions.
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.width = PlayerSettings.WIDTH
        self.height = PlayerSettings.HEIGHT

        self.font = font
        self.font_color = font_color
        self.color = color

        self.active = bool(True)
        self.direction = pg.math.Vector2(0, 0)
        self.side = side
        self.side_trslt = side_trslt
        self.score = int(0)

        quarter_screen_w = self.screen_w // 4
        if self.side == 'left':
            self.side_middle_x = quarter_screen_w
            self.default_pos = (self.WALL_OFFSET, screen_mh)
        else:
            self.side_middle_x = quarter_screen_w * 3
            self.default_pos = (
                self.screen_w - self.width - self.WALL_OFFSET, screen_mh)

        self.update_score_txt()

        # Create the paddle (player).
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(self.color)

        self.rect = self.image.get_rect(midleft=self.default_pos)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.old_rect = self.rect.copy()

    def reset(self) -> None:
        self.reset_direction(True)

        self.rect.midleft = self.default_pos
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.old_rect = self.rect.copy()

        self.score = int(0)
        self.update_score_txt()

    def reset_direction(self, freezed: bool) -> None:
        self.active = freezed
        if freezed:
            self.direction.y = int(0)

    def update_score_txt(self) -> None:
        self.score_txt = self.font.render(
            str(self.score), True, self.font_color)
        score_rect = self.score_txt.get_rect()
        self.score_pos = (self.side_middle_x -
                          score_rect.width//2, self.SCORE_Y_POS)

    def add_point(self) -> None:
        self.score += 1
        self.update_score_txt()

    def draw_hud(self, display: pg.Surface) -> None:
        display.blit(self.score_txt, self.score_pos)

    def check_input(self, keys: pg.key.ScancodeWrapper) -> None:
        self.direction.y = int(0)

        if self.side == 'left':
            if keys[pg.K_z]:
                self.direction.y = -self.VELOCITY
            elif keys[pg.K_s]:
                self.direction.y = self.VELOCITY
            return

        # Right side.
        if keys[pg.K_UP]:
            self.direction.y = -self.VELOCITY
        elif keys[pg.K_DOWN]:
            self.direction.y = self.VELOCITY

    def update(self, dt: float) -> None:
        # Old rect.
        self.old_rect = self.rect.copy()

        if not self.active or self.direction.y == 0:
            return

        # Position.
        self.pos.y += self.direction.y * dt
        self.rect.y = round(self.pos.y)

        # Collisions with wall bottom.
        bottom = self.screen_h - self.WALL_OFFSET
        if self.rect.bottom > bottom:
            self.rect.bottom = bottom
            self.pos.y = self.rect.y

        # Collisions with wall top.
        if self.rect.top < 0 + self.WALL_OFFSET:
            self.rect.top = self.WALL_OFFSET
            self.pos.y = self.rect.y


class Ball(pg.sprite.Sprite):
    VEL_MULTIPLIER = float(62.5)
    VELOCITY = BallSettings.VELOCITY

    def __init__(self, screen_w: int, screen_h: int, screen_mw: int, screen_mh: int, counter_font: pg.font.Font, counter_color: pg.Color, color: pg.Color, group: pg.sprite.Group, player_left: Player, player_right: Player, max_ply_score: int, sounds: list[pg.mixer.Sound]) -> None:
        super().__init__(group)

        # Screen info and players for collisions.
        self.screen_w = screen_w
        self.screen_mw = screen_mw
        self.screen_h = screen_h
        self.player_left = player_left
        self.player_right = player_right
        self.max_player_score = max_ply_score

        # Font.
        self.font = counter_font
        self.font_color = counter_color

        # Sounds.
        self.hit_sound = sounds[0]
        self.score_sound = sounds[1]

        # Movement setup.
        self.vel_x = int(self.VELOCITY * self.VEL_MULTIPLIER)
        self.vel_y = self.vel_x
        self.direction = pg.math.Vector2(
            choice((self.vel_x, -self.vel_x)), choice((self.vel_y, -self.vel_y)))
        self.default_pos = (self.screen_mw, screen_mh)

        # Get ball size.
        width = BallSettings.RADIUS * 2
        size = (width, width)

        # Create the ball surface.
        rect_image = pg.Surface(size, pg.SRCALPHA)
        pg.draw.rect(rect_image, (255, 255, 255),
                     (0, 0, *size), border_radius=BallSettings.RADIUS)

        self.image = pg.Surface(size)
        self.image.fill(color)
        self.image = self.image.convert_alpha()
        self.image.blit(rect_image, (0, 0), None, pg.BLEND_RGBA_MIN)

        # Set the ball on the middle screen.
        self.rect = self.image.get_rect(center=self.default_pos)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.old_rect = self.rect.copy()

        # COUNTDOWN.
        self.freeze_time = int(0)
        self.counter:int = None
        self.active = bool(False)
        self.update_counter(-1)

    def reset(self, winned: bool = False) -> None:
        self.rect.center = self.default_pos
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.old_rect = self.rect.copy()

        if winned:
            self.direction.x = int(choice((self.vel_x, -self.vel_x)))
            self.freeze_time = pg.time.get_ticks()
        else:
            if (self.player_left.score < self.max_player_score and self.player_right.score < self.max_player_score
                    or self.player_right.score < self.max_player_score and self.player_left.score < self.max_player_score):
                self.freeze_time = pg.time.get_ticks()

            self.direction.x *= -1
            self.set_active(False)

        self.direction.y = int(choice((self.vel_y, -self.vel_y)))

    def display_collisions(self, direction: str) -> None:
        if direction == 'vertical':
            if self.rect.top < 0:
                self.hit_sound.play()
                self.rect.top = int(0)
                self.pos.y = self.rect.y
                self.direction.y *= -1
            elif self.rect.bottom > self.screen_h:
                self.hit_sound.play()
                self.rect.bottom = self.screen_h
                self.pos.y = self.rect.y
                self.direction.y *= -1

        if direction == 'horizontal':
            if self.rect.left < 0:
                self.score_sound.play()
                self.player_right.add_point()
                self.reset()

            if self.rect.right > self.screen_w:
                self.score_sound.play()
                self.player_left.add_point()
                self.reset()

    def collisions(self, direction: str):
        overlap_players: list[Player] = []

        if self.rect.colliderect(self.player_left.rect):
            overlap_players.append(self.player_left)

        if self.rect.colliderect(self.player_right.rect):
            overlap_players.append(self.player_right)

        if overlap_players:
            self.hit_sound.play()

            if direction == 'vertical':
                for player in overlap_players:
                    if self.direction.y > 0 and self.rect.bottom >= player.rect.top and self.old_rect.bottom <= player.old_rect.top:
                        self.rect.bottom = int(player.rect.top - 1)
                        self.pos.y = self.rect.y
                        self.direction.y *= -1

                    if self.direction.y < 0 and self.rect.top <= player.rect.bottom and self.old_rect.top >= player.old_rect.bottom:
                        self.rect.top = int(player.rect.bottom + 1)
                        self.pos.y = self.rect.y
                        self.direction.y *= -1

            if direction == 'horizontal':
                for player in overlap_players:
                    if self.direction.x > 0 and self.rect.right >= player.rect.left and self.old_rect.right <= player.old_rect.left:
                        self.rect.right = int(player.rect.left - 1)
                        self.pos.x = self.rect.x
                        self.direction.x *= -1

                    if self.direction.x < 0 and self.rect.left <= player.rect.right and self.old_rect.left >= player.old_rect.right:
                        self.rect.left = int(player.rect.right + 1)
                        self.pos.x = self.rect.x
                        self.direction.x *= -1

        self.display_collisions(direction)

    def set_active(self, state: bool) -> None:
        if state == self.active or type(state) != bool:
            return
        self.active = state

    def update_counter(self, value: int) -> None:
        self.counter = value

        # Create a new counter text surface on update.
        self.counter_txt = self.font.render(
            str(self.counter), True, self.font_color)
        
        self.counter_rect = self.counter_txt.get_rect()
        self.counter_rect.midbottom = (self.screen_mw, self.rect.top - 10)

        self.counter_bg = pg.Rect(self.counter_rect.x, self.counter_rect.y - 3,
                                  self.counter_rect.width, self.counter_rect.height)

    def check_freeze_time(self) -> None:
        current_time = pg.time.get_ticks()
        freezed_time = current_time - self.freeze_time

        if freezed_time <= 700 and self.counter != 3:
            self.update_counter(3)
        if 700 < freezed_time <= 1400 and self.counter != 2:
            self.update_counter(2)
        if 1400 < freezed_time <= 2100 and self.counter != 1:
            self.update_counter(1)
        if freezed_time >= 2100:
            self.set_active(True)
            self.freeze_time = int(0)
            self.update_counter(-1)

    def draw_restart_counter(self, display: pg.Surface, bg_color: pg.Color) -> None:
        pg.draw.rect(display, bg_color, self.counter_bg)
        display.blit(self.counter_txt, self.counter_rect)

    def update(self, dt: float) -> None:
        if self.active:
            # update old rect.
            self.old_rect = self.rect.copy()

            self.pos.x += self.direction.x * dt
            self.rect.x = round(self.pos.x)
            self.collisions('horizontal')

            self.pos.y += self.direction.y * dt
            self.rect.y = round(self.pos.y)
            self.collisions('vertical')
