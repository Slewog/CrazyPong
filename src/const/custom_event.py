from pygame.locals import USEREVENT
from typing import NewType

CustomUserEvent = NewType('CustomUserEvent', int)

CE_BTN_CLICKED = CustomUserEvent(USEREVENT + 1)