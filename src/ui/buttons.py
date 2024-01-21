from typing import Tuple, Dict
import pygame as pg

from ..const.custom_event import CE_BTN_CLICKED
from ..utils import load_color

from ..const.settings import BUTTON

class AnimateButton:
    FONT: pg.font.Font
    FONT_COLOR: pg.Color
    TXT_OFFSET = BUTTON['text_offset']
    
    BORDER_RADIUS = BUTTON['border_radius']
    BORDER_SIZE = BUTTON['border_size']

    CLICK_SOUND: pg.mixer.Sound

    COLORS: dict[str, pg.Color] = {}
    for color_name, color in BUTTON['colors'].items():
        COLORS[color_name] = load_color(color)

    def __init__(self, event_data: Dict[str, str], pos: Tuple[int, int], elevation: int = 5) -> None:
        self.cursor_changed = bool(False)
        self.pressed = bool(False)
        self.hovered = bool(False)
        self.click_time = None

        self.event_data = event_data

        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        self.text_surf = self.FONT.render(event_data['text'], True, self.FONT_COLOR)
        self.text_rect = self.text_surf.get_rect(center=(pos[0], (pos[1] - elevation) + self.TXT_OFFSET))

        self.top_rect = pg.Rect(pos[0], pos[1], self.text_rect.width + BUTTON['width_gap'], self.text_rect.height + BUTTON['height_gap'])
        self.top_rect.center = (pos[0], self.original_y_pos - elevation)
        self.top_rect_color = self.COLORS['top_color']

        self.bottom_rect = pg.Rect(pos[0], pos[1], self.top_rect.width, self.top_rect.height)
        self.bottom_rect.center = pos
    
    def draw(self, display_surf:pg.Surface):
        # Background.
        pg.draw.rect(display_surf, self.COLORS['bg_color'], self.bottom_rect, border_radius=self.BORDER_RADIUS)
        # Top.
        pg.draw.rect(display_surf, self.top_rect_color, self.top_rect, border_radius=self.BORDER_RADIUS)
        # Border.
        pg.draw.rect(display_surf, self.COLORS['bg_color'], self.top_rect, border_radius=self.BORDER_RADIUS, width=self.BORDER_SIZE)

        display_surf.blit(self.text_surf, self.text_rect)

    def change_elevation(self, elevation: int):
        self.dynamic_elevation = elevation

        self.top_rect.center = (self.top_rect.centerx, (self.original_y_pos - self.dynamic_elevation) + self.elevation)
        self.text_rect.center = (self.top_rect.centerx, self.top_rect.centery + self.TXT_OFFSET)

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + elevation
    
    def click(self):
        if self.pressed: 
            return
        
        self.pressed = bool(True)
        self.change_elevation(0)
        self.click_time = pg.time.get_ticks()
        self.CLICK_SOUND.play()

    def check_hover(self, mouse_pos: Tuple[int, int]) -> None:
        if self.top_rect.collidepoint(mouse_pos) or self.bottom_rect.collidepoint(mouse_pos):
            if not self.cursor_changed:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
                self.top_rect_color = self.COLORS['top_color_hover']
                self.cursor_changed = bool(True)
                self.hovered = bool(True)
            return 
        
        self.hovered = bool(False)

        if self.top_rect_color != self.COLORS['top_color']:
            self.top_rect_color = self.COLORS['top_color']
        
        if self.cursor_changed:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
            self.cursor_changed = bool(False)

    def check_click(self):
        if self.click_time is not None:
            current_time = pg.time.get_ticks()

            if current_time - self.click_time >= 125 and self.dynamic_elevation == 0:
                self.change_elevation(self.elevation)

            if current_time - self.click_time >= 200:
                pg.event.post(pg.event.Event(CE_BTN_CLICKED, self.event_data))
                self.pressed = bool(False)
                self.click_time = None