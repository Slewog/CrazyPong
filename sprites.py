import pygame as pg
from random import choice

from settings import BallSettings, PlayerSettings

WHITE = pg.Color('white')


class Player(pg.sprite.Sprite):
    VELOCITY = PlayerSettings.VELOCITY
    WALL_OFFSET = PlayerSettings.WALL_OFFSET

    def __init__(self, side:str, screen_w:int, screen_h:int, groups:pg.sprite.Group) -> None:
        super().__init__(groups)

        # Screen info for collisions.
        self.screen_w = screen_w
        self.screen_h = screen_h
        
        self.direction = pg.math.Vector2()
        self.side = side
        self.score = int(0)

        if self.side == 'left':
            self.default_pos = (10, self.screen_h//2)
        else:
            self.default_pos = (self.screen_w - PlayerSettings.WIDTH - 10, self.screen_h//2)

        # Create the paddle (player).
        self.image = pg.Surface((PlayerSettings.WIDTH, PlayerSettings.HEIGHT))
        self.image.fill(WHITE)

        self.rect = self.image.get_rect(midleft=self.default_pos)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.old_rect = self.rect.copy()

    def check_input(self) -> None:
        keys = pg.key.get_pressed()

        if self.side == 'left':
            if keys[pg.K_z]:
                self.direction.y = -1
            elif keys[pg.K_s]:
                self.direction.y = 1
            else:
                self.direction.y = 0

        if self.side == 'right':
            if keys[pg.K_UP]:
                self.direction.y = -1
            elif keys[pg.K_DOWN]:
                self.direction.y = 1
            else:
                self.direction.y = 0

    def update(self, dt:float) -> None:
        # Old rect.
        self.old_rect = self.rect.copy()

        self.check_input()

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
    VEL_MULTIPLIER = BallSettings.VEL_MULTIPLIER

    def __init__(self, screen_w:int, screen_h:int, group:pg.sprite.Group) -> None:
        super().__init__(group)

        # Screen info for collisions.
        self.screen_w = screen_w
        self.screen_h = screen_h

        # Movement setup.
        self.vel_x = BallSettings.MAX_VELOCITY
        self.vel_y = self.vel_x -1 
        self.direction = pg.math.Vector2(0, 0) # choice((1, -1))
        self.default_pos = (screen_w //2, screen_h // 2)

        # Get ball size.
        width = BallSettings.RADIUS * 2
        size = (width, width)

        # Create the ball surface.
        self.rect_image = pg.Surface(size, pg.SRCALPHA)
        pg.draw.rect(self.rect_image, (255, 255, 255), (0, 0, *size), border_radius=width//2)
        self.image = pg.Surface(size)
        self.image.fill(WHITE)
        self.image = self.image.convert_alpha()
        self.image.blit(self.rect_image, (0, 0), None, pg.BLEND_RGBA_MIN)

        # Set the ball on the middle screen.
        self.rect = self.image.get_rect(center = self.default_pos)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.old_rect = self.rect.copy()

        self.active = False
    
    def display_collisions(self, direction:str) -> None:
        if direction == 'vertical':
            if self.rect.top < 0:
                self.rect.top = 0
                self.pos.y = self.rect.y
                self.direction.y *= -1

            if self.rect.bottom > self.screen_h:
                self.rect.bottom = self.screen_h
                self.pos.y = self.rect.y
                self.direction.y *= -1

        if direction == 'horizontal':
            if self.rect.left < 0:
                self.rect.left = 0
                self.pos.x = self.rect.x
                self.direction.x *= -1
            
            if self.rect.right > self.screen_w:
                self.rect.right = self.screen_w
                self.pos.x = self.rect.x
                self.direction.x *= -1

    def sprite_collision(self, direction:str) -> None:
        overlap_sprites = []

    def collisions(self, direction:str):
        self.sprite_collision(direction)
        self.display_collisions(direction)

    def calcule_speed(self, vel:int, dt:float) -> float:
        return (vel * 65) * dt
    
    def update(self, dt:float) -> None:
        # Check delta time.
        if dt is None or type(dt) != float:
            return
        
        # update old rect.
        self.old_rect = self.rect.copy()

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        if self.direction.x != 0:
            self.pos.x += self.direction.x * self.calcule_speed(self.vel_x, dt)
            self.rect.x = round(self.pos.x)
            self.collisions('horizontal')

        if self.direction.y != 0:
            self.pos.y += self.direction.y * self.calcule_speed(self.vel_y - 1, dt)
            self.rect.y = round(self.pos.y)
            self.collisions('vertical')