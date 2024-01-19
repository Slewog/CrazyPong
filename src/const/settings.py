GAME = {
    'name': str("Py Pong"),
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
    "copyright_pos_offset": int(20),
    'copyright_txt': "Create by Slewog - © 2024",
    'title_txt': GAME['name'],
    "title_pos_offset": int(50),
    'title_txt_size': int(100),
    "btn_offset_centerx": int(175),
    "btn_offset_centery": int(100),
}

BUTTON = {
    'text_offset': int(1),
    'width_gap': int(50),
    'height_gap': int(25),
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