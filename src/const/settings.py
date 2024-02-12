from .custom_typing import ColorValue, UserEvent, DataDict, FontData, SoundDataDict, ButtonSettings, HUDData, CRSData

from pygame import Rect
from pygame.locals import USEREVENT

BTN_CLICKED = UserEvent(USEREVENT + 1)
BALL_OUT_SCREEN = UserEvent(USEREVENT + 2)

FPS = int(120)
GAME_NAME = 'Crazy Pong'
MIDDLE_LINE_W = int(10)
SCREEN_RECT = Rect(0, 0, 1300, 900)
del Rect

FONT_CLR = ColorValue((27, 35, 43, 255))
OBJ_CLR = ColorValue((39, 51, 62, 255))
BG_CLR = ColorValue((70, 80, 90, 255))


FONT: FontData = {
    'family': "freesansbold.ttf",
    'sizes': {
        'default': 30,
        'win_msg': 35,
        'counter': 40,
        'hud': 40,
        'score': 55,
        'title': 100,
    }
}

SOUNDS: SoundDataDict = {
    'ball': {
        'file': "ball_hit.wav",
        'vol': 0.06
    },
    'score': {
        'file': "add_score.wav",
        'vol': 0.07
    },
    'win': {
        'file': "game_win.wav",
        'vol': 0.1
    },
    'button': {
        'file': "btn_click.wav",
        'vol': 0.05
    }
}

BALL = {
    'radius': 14,
    'boost': 5,
    'velocity': 500,
    'max_vel': 850,
    'max_out': 100,
    'start_pos_offset': 100,
}

PADDLE = {
    'velocity': 500,
    'width': 24,
    'height': 160,
    'offset_x': 25,
    'offset_y': 10,
    'max_score': 5,
}

BUTTON_ANIMATE: ButtonSettings = {
    'text_offset': 1,
    'width_gap': 50,
    'height_gap': 25,
    'border_radius': 12,
    'border_size': 3,
    'colors': {
        'font': FONT_CLR,
        'top_color': ColorValue((63, 72, 81, 255)), # '#3F4851'
        'top_color_hover': BG_CLR,
        'bg_color' : FONT_CLR,
    }
}

HUD: HUDData = {
    'score_offset_y': 20,
    'counter_bg_offset': 3,
    'counter_pos_y': SCREEN_RECT.centery - 30,
    'winner_msg_offset': 50,
    'buttons': [
        [
            {'text': "RESTART", 'action': "restart"},
            (SCREEN_RECT.centerx - 130, SCREEN_RECT.centery + 60)
        ],
        [
            {'text': "Back MENU", 'action': "backmenu"},
            (SCREEN_RECT.centerx + 145, SCREEN_RECT.centery + 60)
        ]
    ]
}

CRS_EFFECT: CRSData = {
    'file': "vignette.png",
    'size': SCREEN_RECT.size,
    'line_gap': 4,
    'line_color': ColorValue((20, 20, 20, 255)),
    'min_alpha': 50,
    'max_alpha': 75,
}

STARTING_MENU: DataDict = {
    'texts': [
        {
            'is_title': True,
            'text': GAME_NAME,
            'pos': (SCREEN_RECT.centerx, (SCREEN_RECT.height // 3) - 50),
            'offset_y': 2,
            'center_by': "midtop"
        },
        {
            'is_title': False,
            'text': "Create by Slewog - © 2024",
            'pos': (SCREEN_RECT.centerx, SCREEN_RECT.height - 30),
            'offset_y': 1,
            'center_by': "midbottom"
        }
    ],
    'buttons': [
        [
            {'text': "1 PLAYER", 'action': "play", 'target_level': "oneplayer"},
            (SCREEN_RECT.centerx - 175, SCREEN_RECT.centery)
        ],
        [
            {'text': "2 PLAYER", 'action': "play", 'target_level': "twoplayer"},
            (SCREEN_RECT.centerx + 175, SCREEN_RECT.centery)
        ],
        [
            {'text': "QUIT", 'action': "quit"},
            (SCREEN_RECT.centerx, SCREEN_RECT.centery + 100)
        ]
    ]
}