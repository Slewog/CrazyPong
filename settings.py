class GameSettings:
    SCREEN_W = int(1280)
    SCREEN_H = int(960)
    USE_FPS = bool(True)
    FPS = int(120)
    MAX_SCORE = int(5)
    BACKGROUND_COLOR = str('gray12') # 'gray12' or '#2F373F'
    FONT_COLOR = str('gray79') # (27,35,43) or str('gray79')
    OBJECT_COLOR = str('white')
    HIT_SOUND_VOL = float(0.6)
    SCORE_SOUND_VOL = float(0.6)


class BallSettings:
    DEBUG = bool(True)
    RADIUS = int(14)
    MAX_VELOCITY = int(8)
    Y_VEL_RAND = bool(False)


class PlayerSettings:
    WIDTH = int(12)
    HEIGHT = int(220)
    VELOCITY = int(900)
    WALL_OFFSET = int(10)
    SCORE_Y_POS = int(20)