import pygame as pg
from random import choice

from settings import BallSettings, PlayerSettings


class Player(pg.sprite.Sprite):
    VELOCITY = PlayerSettings.VELOCITY
    WALL_OFFSET = PlayerSettings.WALL_OFFSET
    SCORE_Y_POS = PlayerSettings.SCORE_Y_POS

    def __init__(self, side:str, side_trslt:str, screen_w:int, screen_h:int, group:pg.sprite.Group, font:pg.font.Font, font_color:pg.Color, color:pg.Color) -> None:
        super().__init__(group)

        # Screen info for collisions.
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.width = PlayerSettings.WIDTH
        self.height = PlayerSettings.HEIGHT

        self.font = font
        self.font_color = font_color
        self.color = color

        self.direction = pg.math.Vector2(0, 0)
        self.side = side
        self.side_trslt = side_trslt
        self.score = int(0)
        self.score_pos = (0, 0)
        self.update_score_txt()

        if self.side == 'left':
            self.default_pos = (10, self.screen_h//2)
        else:
            self.default_pos = (self.screen_w - self.width - 10, self.screen_h//2)

        # Create the paddle (player).
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(self.color)

        self.rect = self.image.get_rect(midleft=self.default_pos)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.old_rect = self.rect.copy()

    def reset(self) -> None:
        self.direction.y = 0

        self.rect.midleft = self.default_pos
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.old_rect = self.rect.copy()

        self.score = int(0)
        self.update_score_txt()
    
    def update_score_txt(self) -> None:
        self.score_txt = self.font.render(str(self.score), True, self.font_color)
        score_rect = self.score_txt.get_rect()

        self.score_pos = self.side == 'left' and (self.screen_w//4 - score_rect.width//2, self.SCORE_Y_POS) or (self.screen_w*3//4 - score_rect.width//2, self.SCORE_Y_POS)
    
    def add_point(self) -> None:
        self.score += 1
        self.update_score_txt()
    
    def draw_hud(self, display:pg.Surface) -> None:
        display.blit(self.score_txt, self.score_pos)

    def check_input(self, keys:pg.key.ScancodeWrapper) -> None:
        if self.side == 'left':
            if keys[pg.K_z]:
                self.direction.y = -1
            elif keys[pg.K_s]:
                self.direction.y = 1
            else:
                self.direction.y = 0
        elif self.side == 'right':
            if keys[pg.K_UP]:
                self.direction.y = -1
            elif keys[pg.K_DOWN]:
                self.direction.y = 1
            else:
                self.direction.y = 0

    def update(self, dt:float) -> None:
        # Old rect.
        self.old_rect = self.rect.copy()

        # Position.
        if self.direction.y != 0:
            self.pos.y += self.direction.y * self.VELOCITY * dt
            self.rect.y = round(self.pos.y)
        
        # Collisions with wall bottom.
        if self.rect.bottom > self.screen_h - self.WALL_OFFSET:
            self.rect.bottom = self.screen_h - self.WALL_OFFSET
            self.pos.y = self.rect.y
        
        # Collisions with wall top.
        if self.rect.top < self.WALL_OFFSET:
            self.rect.top = self.WALL_OFFSET
            self.pos.y = self.rect.y


class Ball(pg.sprite.Sprite):
    DEBUG = BallSettings.DEBUG
    VEL_MULTIPLIER = int(65)
    Y_VEL_RAND = BallSettings.Y_VEL_RAND

    def __init__(self, screen_w:int, screen_h:int, color:pg.Color, group:pg.sprite.Group, player_left:Player, player_right:Player, sounds:list[pg.mixer.Sound]) -> None:
        super().__init__(group)

        # Screen info and players for collisions.
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.player_left = player_left
        self.player_right = player_right
        self.last_wall = str("")

        # Sounds.
        self.hit_sound = sounds[0]
        self.score_sound = sounds[1]

        # Movement setup.
        self.vel_x = BallSettings.MAX_VELOCITY
        self.vel_y = self.vel_x - 1
        self.direction = pg.math.Vector2(choice((1, -1)), choice((1, -1)))
        self.default_pos = (screen_w //2, screen_h // 2)

        # Get ball size.
        width = BallSettings.RADIUS * 2
        size = (width, width)

        # Create the ball surface.
        self.rect_image = pg.Surface(size, pg.SRCALPHA)
        pg.draw.rect(self.rect_image, (255, 255, 255), (0, 0, *size), border_radius=width//2)
        self.image = pg.Surface(size)
        self.image.fill(color)
        self.image = self.image.convert_alpha()
        self.image.blit(self.rect_image, (0, 0), None, pg.BLEND_RGBA_MIN)

        # Set the ball on the middle screen.
        self.rect = self.image.get_rect(center = self.default_pos)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.old_rect = self.rect.copy()

    def reset(self, winned:bool=False) -> None:
        self.rect.center = self.default_pos
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.old_rect = self.rect.copy()

        if winned:
            self.direction.x = choice((1, -1))
        else:
            self.direction.x *= -1
        self.direction.y = choice((1, -1))

        if self.Y_VEL_RAND:
            self.vel_y = self.vel_x - 1

        self.last_wall = str("")

    def calcule_vel_y(self, sprite:Player) -> None:
        # Calcule new Y vel from difference in Y pos with the ball and a player paddle.
        if not self.Y_VEL_RAND:
            return
        
        # Remove one from max vel to get a smooth movement from ball (only if SAME_VEL_AXIS is False).
        max_vel = float(self.vel_x - 1) 
        difference_in_y = float(sprite.rect.center[1] - self.rect.center[1])
        reduction_factor = float((sprite.height / 2) / max_vel)
        self.vel_y = (difference_in_y / reduction_factor)
        
        if self.vel_y < 0:
            self.vel_y *= -1

    def calcule_speed(self, vel:int, dt:float) -> float:
        return (vel * self.VEL_MULTIPLIER) * dt  

    def display_collisions(self, direction:str) -> None:
        if direction == 'vertical':
            if self.rect.top < 0 and self.last_wall != 'top':
                self.hit_sound.play()
                self.rect.top = int(0)
                self.pos.y = self.rect.y
                self.direction.y *= -1
                self.last_wall = str("top")
            elif self.rect.bottom > self.screen_h and self.last_wall != 'bottom':
                self.hit_sound.play()
                self.rect.bottom = self.screen_h
                self.pos.y = self.rect.y
                self.direction.y *= -1
                self.last_wall = str("bottom")
            else:
                self.last_wall = str("")

        if direction == 'horizontal':
            if self.rect.left < 0:
                self.score_sound.play()
                if self.DEBUG:
                    self.rect.left = 0
                    self.pos.x = self.rect.x
                    self.direction.x *= -1
                    return
                self.player_right.add_point()
                self.reset()
            
            if self.rect.right > self.screen_w:
                self.score_sound.play()
                self.player_left.add_point()
                self.reset()

    def collisions(self, direction:str):
        overlap_sprites:list[pg.sprite.Sprite] = []

        if self.rect.colliderect(self.player_left.rect):
            overlap_sprites.append(self.player_left)
        
        if self.rect.colliderect(self.player_right.rect):
            overlap_sprites.append(self.player_right)

        if overlap_sprites:
            self.hit_sound.play()

            if direction == 'vertical':
                for sprite in overlap_sprites:
                    if self.direction.y > 0 and self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top - 1
                        self.pos.y = self.rect.y
                        self.direction.y *= -1

                    if self.direction.y < 0 and self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom + 1
                        self.pos.y = self.rect.y
                        self.direction.y *= -1

            if direction == 'horizontal':
                for sprite in overlap_sprites:
                    if self.direction.x > 0 and self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left - 1
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                        self.calcule_vel_y(sprite)
                    
                    if self.direction.x < 0 and self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right + 1
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                        self.calcule_vel_y(sprite)
    
        self.display_collisions(direction)

    def update(self, dt:float) -> None:
        # update old rect.
        self.old_rect = self.rect.copy()

        if self.direction.x != 0:
            self.pos.x += self.direction.x * self.calcule_speed(self.vel_x, dt)
            self.rect.x = round(self.pos.x)
            self.collisions('horizontal')

        if self.direction.y != 0:
            self.pos.y += self.direction.y * self.calcule_speed(self.vel_y, dt)
            self.rect.y = round(self.pos.y)
            self.collisions('vertical')