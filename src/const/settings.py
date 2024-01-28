from .custom_typing import GameData, BallData, PaddleData, ColorValue, HUDData, SoundDict
from .custom_typing import CRSData, FontData, ButtonData, MenuTitleData, UserEvent

from typing import Dict
from pygame import Rect
from pygame.locals import USEREVENT

SCREEN_RECT = Rect(0, 0, 1300, 900)
CE_BTN_CLICKED = UserEvent(USEREVENT + 1)
CE_BALL_OUT_SCREEN = UserEvent(USEREVENT + 2)

GAME: GameData = {
    'name': "Crazy Pong",
    'fps': 120,
    'middle_rect_w': 10,
}

HUD: HUDData = {
    'score_offset_y': 20,
    'counter_bg_offset': 2,
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

FONT: FontData = {
    'family': "freesansbold.ttf",
    'from_system': False,
    'default_size': 30,
    'title_size': 100,
    'hud_size': 40,
    'score_size': 55,
}

COLORS: Dict[str, ColorValue] = {
    'font': (27, 35, 43, 255),
    'objects': "#27333E",
    'background': "#46505A",
}

SOUNDS: SoundDict = {
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
    }
}

CRS_EFFECT: CRSData = {
    'file': "vignette.png",
    'line_gap': 4,
    'line_color': (20, 20, 20),
    'min_alpha': 50,
    'max_alpha': 75,
}

BALL: BallData = {
    'radius': 12,
    'boost': 5,
    'velocity': 500,
    'max_vel': 650,
    'max_out': 100,
    'start_pos_offset': 100
}

PADDLE: PaddleData = {
    'width': 24,
    'height': 160,
    'velocity': 500,
    'offset_x': 25,
    'offset_y': 10,
    'max_score': 5,
}

BUTTON_ANIMATE: ButtonData = {
    'text_offset': 1,
    'width_gap': 50,
    'height_gap': 25,
    'border_radius': 12,
    'border_size': 3,
    'sound_vol': 0.05,
    'sound_file': "btn_click.wav",
    'colors': {
        'top_color': "#3F4851",
        'top_color_hover': COLORS['background'],
        'bg_color' : COLORS['font'],
    }
}

STARTING_MENU: MenuTitleData = {
    'title': {
        'text': GAME['name'],
        'pos': (SCREEN_RECT.centerx, (SCREEN_RECT.height // 3) - 50),
        'center_by': "midtop"
    },
    'copyright': {
        'text': "Create by Slewog - © 2024",
        'pos': (SCREEN_RECT.centerx, SCREEN_RECT.height - 20),
        'center_by': "midbottom"
    },
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