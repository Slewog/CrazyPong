from typing import Tuple, Dict, List

from pygame.locals import SYSTEM_CURSOR_HAND, SYSTEM_CURSOR_ARROW
from pygame import Surface, Rect, draw, time, mouse, event
from pygame.font import Font
from pygame.mixer import Sound

from src.const.settings import BUTTON_ANIMATE, BTN_CLICKED


class ButtonAnimate:
    TXT_OFFSET = BUTTON_ANIMATE['text_offset']
    BORDER_RADIUS = BUTTON_ANIMATE['border_radius']
    BORDER_SIZE = BUTTON_ANIMATE['border_size']
    COLORS = BUTTON_ANIMATE['colors'].copy()

    FONT: Font
    CLICK_SOUND: Sound

    def __init__(self, data: Dict[str, str], pos: Tuple[int, int], elevation: int = 5) -> None:
        self.pressed = bool(False)
        self.hovered = bool(False)
        self.click_time = None

        self.data = data

        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        self.text_surf = self.FONT.render(data['text'], True, self.COLORS['font'])
        self.text_rect = self.text_surf.get_rect(center=(pos[0], (pos[1] - elevation) + self.TXT_OFFSET))

        self.top_rect = Rect(
            pos[0],
            pos[1],
            self.text_rect.width + BUTTON_ANIMATE['width_gap'],
            self.text_rect.height + BUTTON_ANIMATE['height_gap']
        )
        self.top_rect.center = (pos[0], self.original_y_pos - elevation)
        self.top_rect_color = self.COLORS['top_color']

        self.bottom_rect = Rect(pos[0], pos[1], self.top_rect.width, self.top_rect.height + elevation)
        self.bottom_rect.center = pos

    def change_elevation(self, elevation: int) -> None:
        self.dynamic_elevation = elevation

        self.top_rect.center = (self.top_rect.centerx, (self.original_y_pos - self.dynamic_elevation) + self.elevation)
        self.text_rect.center = (self.top_rect.centerx, self.top_rect.centery + self.TXT_OFFSET)

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + elevation
    
    def click(self) -> None:
        if self.pressed: return
        
        self.pressed = not self.pressed
        self.change_elevation(0)
        self.click_time = time.get_ticks()
        self.CLICK_SOUND.play()

    def check_hover(self, mouse_pos: Tuple[int, int]) -> None:
        collide = self.top_rect.collidepoint(mouse_pos)
        
        if not self.hovered and collide:
            mouse.set_cursor(SYSTEM_CURSOR_HAND)
            self.top_rect_color = self.COLORS['top_color_hover']
            self.hovered = not self.hovered
                    
        if self.hovered and not collide:
            mouse.set_cursor(SYSTEM_CURSOR_ARROW)
            self.top_rect_color = self.COLORS['top_color']
            self.hovered = not self.hovered

    def check_click(self) -> None:
        if self.click_time is None: return
        
        clicked_time = time.get_ticks() - self.click_time

        if clicked_time >= 125 and self.dynamic_elevation == 0:
            self.change_elevation(self.elevation)

        if clicked_time >= 200:
            event.post(event.Event(BTN_CLICKED, self.data))
            self.pressed = bool(False)
            self.click_time = None
    
    def render(self, display_surf: Surface, mouse_pos: Tuple[int, int]) -> None:
        self.check_hover(mouse_pos)
        self.check_click()

        # Background.
        draw.rect(display_surf, self.COLORS['bg_color'], self.bottom_rect, border_radius=self.BORDER_RADIUS)
        # Top.
        draw.rect(display_surf, self.top_rect_color, self.top_rect, border_radius=self.BORDER_RADIUS)
        # Border.
        draw.rect(display_surf, self.COLORS['bg_color'], self.top_rect, border_radius=self.BORDER_RADIUS, width=self.BORDER_SIZE)

        display_surf.blit(self.text_surf, self.text_rect)


ButtonList = List[ButtonAnimate]