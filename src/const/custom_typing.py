from typing import TypedDict, NewType, Tuple, Dict, List
from pygame.font import Font

UserEvent = NewType('UserEvent', int)
CollisionValue = Tuple[bool, str, str]
ColorValue = NewType('ColorValue', Tuple[int, int, int, int])
DataDict = Dict[str, List]
FontsDict = Dict[str, Font]


class HUDData(TypedDict):
    counter_bg_offset: int
    counter_pos_y: int
    score_offset_y: int
    winner_msg_offset: int
    buttons: DataDict


class SoundData(TypedDict):
    file: str
    vol: float


class SoundDataDict(TypedDict):
    ball: SoundData
    win: SoundData
    score: SoundData
    button: SoundData


class FontData(TypedDict):
    family: str
    sizes: Dict[str, int]


class ButtonSettings(TypedDict):
    text_offset: int
    width_gap: int
    height_gap: int
    border_radius: int
    border_size: int
    colors: Dict[str, ColorValue]


class TextData(TypedDict):
    is_title: bool
    text: str
    pos: Tuple[int, int]
    offset_y: int
    center_by: str


class CRSData(TypedDict):
    file: str
    size: Tuple[int, int]
    line_gap: int
    line_color: ColorValue
    min_alpha: int
    max_alpha: int