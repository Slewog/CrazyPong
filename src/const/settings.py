GAME = {
    'name': "Py Pong",
    'fps': int(120),
    'width': int(1280),
    'height': int(960)
}

FONT = {
    'family': str('freesansbold.ttf'),
    'from_system': bool(False),
    'size': int(30)
}

MENU = {
    'copyright_txt': "Create by Slewog",
    'title_txt': GAME['name'],
    'title_txt_size': int(100)
}

BUTTON = {
    'text_offset': 1,
    'border_radius': int(12),
    'border_size': int(5),
    'sound_vol': 0.05,
    'colors': {
        'font': (27, 35, 43, 255),
        'top_color': '#3F4851',
        'top_color_hover': '#46505A',
        'bg_color' : (27, 35, 43, 255),
    }
}

COLORS = {
    'font': (27, 35, 43, 255),
    'objects': str('#27333E'),
    'background': str('#46505A'),
}