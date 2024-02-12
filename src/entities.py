from pygame.font import Font
from pygame.mixer import Sound
from pygame.math import Vector2
from pygame.key import ScancodeWrapper
from pygame import Surface, sprite, event, draw
from pygame.locals import K_r, K_f, K_UP, K_DOWN, SRCALPHA

from .const.settings import BALL, PADDLE, OBJ_CLR, SCREEN_RECT
from .const.settings import BALL_OUT_SCREEN, HUD, FONT_CLR

from random import choice, randint

class Score(sprite.Sprite):
    FONT: Font
    FONT_COLOR = FONT_CLR
    OFFSET_Y = HUD['score_offset_y']

    def __init__(self, pos_x: int, group: sprite.Group) -> None:
        sprite.Sprite.__init__(self, group)
        
        self.pos_x = pos_x
        self.current = int(4)
        self.update_surf()

    def update_surf(self) -> None:
        self.image = self.FONT.render(str(self.current), True, self.FONT_COLOR)
        self.rect = self.image.get_rect(midtop=(self.pos_x, self.OFFSET_Y))

    def reset(self) -> None:
        self.current = int(0)
        self.update_surf()

    def add_point(self) -> None:
        self.current += 1
        self.update_surf()


class Paddle(sprite.Sprite):
    MAX_SCORE = PADDLE['max_score']
    OFFSET_X = PADDLE['offset_x']
    VELOCITY = PADDLE['velocity']
    WIDTH = PADDLE['width']
    HEIGHT = PADDLE['height']
    H_WIDTH = WIDTH // 2
    H_HEIGHT = HEIGHT // 2

    MIN_Y = (H_HEIGHT) + PADDLE['offset_y']
    MAX_Y = SCREEN_RECT.height - (H_HEIGHT) - (PADDLE['offset_y'] - 1)

    def __init__(self, side: str, paddle_type: str, hud_pos_x: int, group: sprite.Group) -> None:
        sprite.Sprite.__init__(self, group)
        
        self.image = Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(OBJ_CLR)

        self.type = paddle_type
        self.side = side
        self.score = Score(hud_pos_x, group)

        if side == 'left':
            self.default_pos = (
                self.H_WIDTH + self.OFFSET_X, 
                SCREEN_RECT.centery
            )
            self.K_UP = K_r
            self.K_DOWN = K_f
        else:
            self.default_pos = (
                SCREEN_RECT.width - (self.H_WIDTH) - self.OFFSET_X,
                SCREEN_RECT.centery
            )
            self.K_UP = K_UP
            self.K_DOWN = K_DOWN

        self.rect = self.image.get_rect(center=self.default_pos)
        self.pos = Vector2(self.rect.center)

    def winned(self) -> bool:
        return self.score.current >= self.MAX_SCORE

    def reset(self):
        self.rect = self.image.get_rect(center=self.default_pos)
        self.pos = Vector2(self.rect.center)

        self.score.reset()

    def destroy(self):
        self.score.kill()
        self.kill()
    
    def update(self, dt: float, keys: ScancodeWrapper, ball: 'Ball') -> None:
        if self.type == 'player':
            # Move and clamp the paddle inside the screen.
            if keys[self.K_UP]:
                self.pos.y = max(self.MIN_Y, self.pos.y - (self.VELOCITY * dt))
            if keys[self.K_DOWN]:
                self.pos.y = min(self.MAX_Y, self.pos.y + (self.VELOCITY * dt))

        if self.type == 'ai':
            dist = self.rect.centery - ball.pos.y
            ai_movement = self.VELOCITY * dt

            if abs(dist) > ai_movement:
                # Move and clamp the paddle inside the screen.
                if dist > 0:
                    self.pos.y = max(self.MIN_Y, self.pos.y - ai_movement)
                else:
                    self.pos.y = min(self.MAX_Y, self.pos.y + ai_movement)

        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)


class Ball(sprite.Sprite):
    velocity = BALL['velocity']
    MAX_VELOCITY = BALL['max_vel']
    BOOST = BALL['boost']
    RADIUS = BALL['radius']
    SIZE = RADIUS * 2
    RADIUS_SQ = RADIUS ** 2

    MIN_X = -BALL['max_out']
    MAX_X = SCREEN_RECT.width + BALL['max_out']
    MIN_Y = int(0)
    MAX_Y = SCREEN_RECT.height
    START_OFFSET = BALL['start_pos_offset']
    START_OFFSET_MAX = SCREEN_RECT.height - START_OFFSET

    HIT_SOUND: Sound

    def __init__(self, group: sprite.GroupSingle) -> None:
        sprite.Sprite.__init__(self, group)

        self.active = bool(False)

        self.image = Surface((self.SIZE, self.SIZE), SRCALPHA)
        draw.circle(self.image, OBJ_CLR, (self.RADIUS, self.RADIUS), radius=self.RADIUS)

        self.rect = self.image.get_rect(center=self.get_random_position())
        self.pos = Vector2(self.rect.center)

        self.direction = Vector2(
            self.get_random_direction(),
            self.get_random_direction()
        )

    def set_active(self, state: bool) -> None:
        if state == self.active or type(state) != bool:
            return
        self.active = state

    def reset(self, full: bool = False):
        self.velocity = BALL['velocity']
        self.rect.center = self.get_random_position()
        self.pos = Vector2(self.rect.center)

        self.set_active(False)

        if not full:
            self.direction.x *= -1
            self.direction.y = self.get_random_direction()
        else:
            self.direction.x = self.get_random_direction()
            self.direction.y = self.get_random_direction()

    def play_sfx(self):
        self.HIT_SOUND.play()

    def speed_up(self):
        if self.velocity < self.MAX_VELOCITY - self.BOOST:
            self.velocity += self.BOOST
            return

        if self.MAX_VELOCITY - self.BOOST < self.velocity < self.MAX_VELOCITY:
            self.velocity += 1

    def get_random_direction(self) -> int:
        """Return -1 or 1"""
        return choice((-1, 1))

    def get_random_position(self):
        return (
            SCREEN_RECT.centerx,
            randint(self.START_OFFSET, self.START_OFFSET_MAX)
        )

    def check_wall_collision(self):
        # Left.
        if self.pos.x - self.RADIUS < self.MIN_X:
            event.post(event.Event(BALL_OUT_SCREEN, {'target': 'right'}))
        
        # Right.
        if self.pos.x + self.RADIUS > self.MAX_X:
            event.post(event.Event(BALL_OUT_SCREEN, {'target': 'left'}))

        # Top.
        if self.pos.y - self.RADIUS < self.MIN_Y:
            self.play_sfx()
            self.pos.y = self.RADIUS + self.MIN_Y
            self.direction.y *= -1
        
        # Bottom.
        if self.pos.y + self.RADIUS > self.MAX_Y:
            self.play_sfx()
            self.pos.y = self.MAX_Y - self.RADIUS
            self.direction.y *= -1

    def paddle_collision(self, side: str, corner: str, dist_x: int, dist_y: int, paddle: Paddle):
        if side:
            if side in ['top', 'bottom']:
                if side == 'top':
                    self.pos.y = max(paddle.rect.top - self.RADIUS, self.RADIUS + self.MIN_Y)
                    paddle.rect.top = int(self.pos.y) + self.RADIUS
                    paddle.pos.y = paddle.rect.centery
                else:
                    self.pos.y = min(paddle.rect.bottom + self.RADIUS, self.MAX_Y - self.RADIUS)
                    paddle.rect.bottom = int(self.pos.y) - self.RADIUS
                    paddle.pos.y = paddle.rect.centery
                
                # Reflect the movement of the ball only if its movement vector points in a direction "against" the ball
                if (dist_y < 0 and self.direction.y > 0) or (dist_y > 0 and self.direction.y < 0):
                    self.direction.reflect_ip((0, 1))
                    self.play_sfx()

            if side in ['left', 'right']:
                if side == 'left':
                    self.pos.x = max(paddle.rect.left - self.RADIUS, self.RADIUS + self.MIN_X)
                else:
                    self.pos.x = min(paddle.rect.right + self.RADIUS, self.MAX_X - self.RADIUS)

                # Reflect the movement of the ball only if its movement vector points in a direction "against" the ball
                if (dist_x < 0 and self.direction.x > 0) or (dist_x > 0 and self.direction.x < 0):
                    self.direction.reflect_ip((1, 0))
                    self.play_sfx()
                    self.speed_up()
        
        if corner:
            self.play_sfx()

            if corner == 'topleft' and self.direction.y > 0 and self.direction.x > 0:
                self.direction.x *= -1
                self.direction.y *= -1
            elif corner == 'bottomleft' and self.direction.y < 0 and self.direction.x > 0:
                self.direction.x *= -1
                self.direction.y *= -1
            elif corner == 'topright' and self.direction.y > 0 and self.direction.x < 0:
                self.direction.x *= -1
                self.direction.y *= -1
            elif corner == 'bottomright' and self.direction.y < 0 and self.direction.x < 0:
                self.direction.x *= -1
                self.direction.y *= -1
        
        # /!\ Refresh ball rect after collision has been treated avoid collision bug ans draw it correctly on screen. /!\
        self.rect.center = int(self.pos.x), int(self.pos.y)

    def update(self, dt: float) -> None:
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.velocity * self.direction.x * dt
        self.pos.y += self.velocity * self.direction.y * dt

        self.check_wall_collision()

        self.rect.center = int(self.pos.x), int(self.pos.y)