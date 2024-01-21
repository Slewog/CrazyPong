from pygame.locals import USEREVENT
from typing import NewType

CustomUserEvent = NewType('CustomUserEvent', int)

# Event call when a button is clicked.
CE_BTN_CLICKED = CustomUserEvent(USEREVENT + 1)

# Event call when the ball collide with the left or right of the display.
CE_BALL_OUT_SCREEN = CustomUserEvent(USEREVENT + 2)