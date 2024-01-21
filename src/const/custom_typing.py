from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict, Dict, Union, Tuple, List

if TYPE_CHECKING:
    from pygame import Surface, Color, Rect

ColorValue = Union[str, Tuple[int, int, int], List[int]]

class GameData(TypedDict):
    name: str
    fps: int
    width: int
    height: int
    middle_rect_w: int


class SoundData(TypedDict):
    file: str
    vol: float | int


class FontData(TypedDict):
    family: str
    size: int
    from_system: bool


class ButtonData(TypedDict):
    text_offset: int
    width_gap: int
    height_gap: bool
    border_radius: int
    border_size: int
    sound_vol: int
    sound_file: int
    colors: Dict


class CRSData(TypedDict):
    file: str
    vignette:Surface
    line_gap: int
    line_color: Color
    min_alpha: int
    max_alpha: int
    screen_rect: Rect