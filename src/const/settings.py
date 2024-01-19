GAME = {
    'name': str("Py Pong"),
    'fps': int(60),
    'width': int(1280),
    'height': int(960)
}

FONT = {
    'family': str("freesansbold.ttf"),
    'from_system': bool(False),
    'size': int(30)
}

COLORS = {
    'font': (27, 35, 43, 255),
    'objects': str("#27333E"),
    'background': str("#46505A"),
}

BUTTON = {
    'text_offset': int(1),
    'width_gap': int(50),
    'height_gap': int(25),
    'border_radius': int(12),
    'border_size': int(5),
    'sound_vol': 0.05,
    'colors': {
        'top_color': "#3F4851",
        'top_color_hover': COLORS['background'],
        'bg_color' : COLORS['font'],
    }
}

MENU = {
    'title': {
        'text': GAME['name'],
        'font_size': int(100),
        'pos': (GAME['width'] // 2, (GAME['height'] // 3) - int(50))
    },
    'copyright': {
        'text': str("Create by Slewog - © 2024"),
        'pos': (GAME['width'] // 2, GAME['height'] - int(20))
    },
    'pg_logo': {
        'file': "pygame_logo.png",
        'pos': (GAME['width'] - 10, GAME['height'] - 9)
    },
    'buttons': [
        [
            {'text': "1 PLAYER", 'action': "play", 'target_level': 'oneplayer'},
            (GAME['width'] // 2 - 175, GAME['height'] // 2)
        ],
        [
            {'text': "2 PLAYER", 'action': "play", 'target_level': 'twoplayer'},
            (GAME['width'] // 2 + 175, GAME['height'] // 2)
        ],
        [
            {'text': "QUIT", 'action': "quit", 'target_level': None},
            (GAME['width'] // 2, GAME['height'] // 2 + 100)
        ]
    ]
}

BALL = {
    'radius': int(14),
    'velocity': int(435)
}