from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict, NewType, Dict, Union, Tuple, List

if TYPE_CHECKING:
    from pygame import Surface, Color, Rect

UserEvent = NewType('UserEvent', int)
ColorValue = Union[str, Tuple[int, int, int], List[int]]


class GameData(TypedDict):
    name: str
    fps: int
    middle_rect_w: int


class HUDData(TypedDict):
    counter_bg_offset: int
    counter_pos_y: int
    score_offset_y: int
    winner_msg_offset: int
    buttons: List[List]


class BallData(TypedDict):
    radius: int
    boost: int
    velocity: int
    max_vel : int
    max_out: int
    start_pos_offset: int


class PaddleData(TypedDict):
    width: int
    height: int
    offset_x: int
    offset_y: int
    velocity: int
    max_score: int


class SoundData(TypedDict):
    file: str
    vol: float | int


class SoundDict(TypedDict):
    ball: SoundData
    win: SoundData
    score: SoundData


class FontData(TypedDict):
    family: str
    default_size: int
    from_system: bool
    title_size: int
    hud_size: int
    score_size: int


class ButtonData(TypedDict):
    text_offset: int
    width_gap: int
    height_gap: int
    border_radius: int
    border_size: int
    sound_vol: float
    sound_file: str
    colors: Dict[str, ColorValue]


class CRSData(TypedDict):
    file: str
    vignette: Surface
    line_gap: int
    line_color: Color
    min_alpha: int
    max_alpha: int
    screen_rect: Rect


class TextData(TypedDict):
    text: str
    pos: Tuple[int, int]
    center_by: str


class MenuTitleData(TypedDict):
    title: TextData
    copyright: TextData
    buttons: List[List]