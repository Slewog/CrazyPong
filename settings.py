class GameSettings:
    SCREEN_W = int(1280)
    SCREEN_H = int(720)
    USE_FPS = bool(False)
    FPS = int(60)
    MAX_SCORE = int(5)


class BallSettings:
    RADIUS = int(14)
    MAX_VELOCITY = int(8)
    VEL_MULTIPLIER = int(65)


class PlayerSettings:
    WIDTH = int(12)
    HEIGHT = int(220)
    VELOCITY = int(450)
    WALL_OFFSET = int(10)