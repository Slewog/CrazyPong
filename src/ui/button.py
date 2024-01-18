import pygame as pg


class Button:
    def __init__(self, data) -> None:
        self.cursor_changed = False
        self.pressed = False