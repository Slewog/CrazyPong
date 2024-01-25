from .custom_typing import GameData, BallData, PaddleData, ColorValue, HUDData, SoundDict
from .custom_typing import CRSData, FontData, ButtonData, MenuTitleData
from typing import Dict
from pygame import Rect

SCREEN_RECT = Rect(0, 0, 1280, 960)

GAME: GameData = {
    'name': "Py Pong",
    'fps': 120,
    'width': 1280,
    'height': 960,
    'middle_rect_w': 6,
}

HUD: HUDData = {
    'score_offset_y': 20,
    'counter_bg_offset': 2,
    'counter_offset_y': 10,
    'winner_msg_offset': 50,
    'buttons': [
        [
            {'text': "RESTART", 'action': "restart"},
            (GAME['width'] // 2 - 130, GAME['height'] // 2 + 60)
        ],
        [
            {'text': "Back MENU", 'action': "backmenu"},
            (GAME['width'] // 2 + 145, GAME['height'] // 2 + 60)
        ]
    ]
}

FONT: FontData = {
    'family': "freesansbold.ttf",
    'from_system': False,
    'default_size': 30,
    'title_size': 100,
    'hud_size': 40
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
    'max_alpha': 70
}

BALL: BallData = {
    'radius': 14,
    'velocity': 450,
    'min_coll_tol': 2,
    'max_coll_tol': 10,
    'starting_pos': (SCREEN_RECT.centerx, SCREEN_RECT.centery)
}

PADDLE: PaddleData = {
    'width': 36,
    'height': 160,
    'velocity': 500,
    'ai_vel_debuff': 100,
    'offset_x': 20,
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
        'pos': (GAME['width'] // 2, (GAME['height'] // 3) - 50),
        'center_by': "midtop"
    },
    'copyright': {
        'text': "Create by Slewog - © 2024",
        'pos': (GAME['width'] // 2, GAME['height'] - 20),
        'center_by': "midbottom"
    },
    'pg_logo': {
        'file': "pygame_logo.png",
        'pos': (GAME['width'] - 10, GAME['height'] - 9)
    },
    'buttons': [
        [
            {'text': "1 PLAYER", 'action': "play", 'target_level': "oneplayer"},
            (GAME['width'] // 2 - 175, GAME['height'] // 2)
        ],
        [
            {'text': "2 PLAYER", 'action': "play", 'target_level': "twoplayer"},
            (GAME['width'] // 2 + 175, GAME['height'] // 2)
        ],
        [
            {'text': "QUIT", 'action': "quit"},
            (GAME['width'] // 2, GAME['height'] // 2 + 100)
        ]
    ]
}