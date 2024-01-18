import pygame as pg


class Button:
    FONT: pg.font.Font
    FONT_COLOR: pg.Color
    BORDER_COLOR: pg.Color
    BACKGROUND_COLOR: pg.Color

    RADIUS: int
    BORDER_SIZE = int(5)
    CLICK_SOUND = pg.mixer.Sound

    def __init__(self, data: dict, pos: tuple[int, int], elevation: int = 5) -> None:
        self.cursor_changed = False
        self.pressed = False
        self.action = data['action']
        self.type = data['type']

        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        self.text_offset = int(1)
        self.text_surf = self.FONT.render(data['text'], True, self.FONT_COLOR)
        self.text_rect = self.text_surf.get_rect(center=(pos[0], (pos[1] - elevation) + self.text_offset))

        self.top_rect = pg.Rect(pos[0], pos[1], self.text_rect.width + 50, self.text_rect.height + 25)
        self.top_rect.center = (pos[0], self.original_y_pos - elevation)
        self.top_rect_color = self.BACKGROUND_COLOR

        self.bottom_rect = pg.Rect(pos[0], pos[1], self.top_rect.width, self.top_rect.height)
        self.bottom_rect.center = pos
    
    def draw(self, display_surf:pg.Surface):
        # Background.
        pg.draw.rect(display_surf, self.BORDER_COLOR, self.bottom_rect, border_radius=self.RADIUS)
        # Top.
        pg.draw.rect(display_surf, self.top_rect_color, self.top_rect, border_radius=self.RADIUS)
        # Border.
        pg.draw.rect(display_surf, self.BORDER_COLOR, self.top_rect, border_radius=self.RADIUS, width=self.BORDER_SIZE)

        display_surf.blit(self.text_surf, self.text_rect)

    def change_elevation(self, elevation: int):
        self.dynamic_elevation = elevation

        self.top_rect.center = (self.top_rect.centerx, (self.original_y_pos - self.dynamic_elevation) + self.elevation)
        self.text_rect.center = (self.top_rect.centerx, self.top_rect.centery + self.text_offset)

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + elevation

    def is_hovered(self, mouse_pos: tuple[int, int]):
        if self.top_rect.collidepoint(mouse_pos):
            if not self.cursor_changed:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
                self.cursor_changed = True
            return True
        
        if self.cursor_changed:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
            self.cursor_changed = False

        if self.pressed:
            self.pressed = False

        if self.dynamic_elevation == 0:
            self.change_elevation(self.elevation)

        return False
        
    def is_clicked(self):
        left_btn_down_click = pg.mouse.get_pressed()[0]

        if self.pressed and not left_btn_down_click:
            self.change_elevation(self.elevation)
            self.pressed = False
            pg.time.wait(100)
            return True

        if not self.pressed and left_btn_down_click:
            self.pressed = True
            self.change_elevation(0)

        return False