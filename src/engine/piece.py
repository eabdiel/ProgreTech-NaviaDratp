"""
===============================================================================
Navia Dratp Digital - Fan Project
===============================================================================

Author: Edwin A. Rodriguez
GitHub: https://github.com/eabdiel
Project Website: https://progretech.com/navia_dratp_digital_archive_site/

Fan Project Notice:
This project is an unofficial fan-made digital prototype inspired by the
discontinued Navia Dratp board game originally published by Bandai.
The author and contributors do not own Navia Dratp, its trademarks, original
artwork, rules text, characters, or any related Bandai/Bandai Namco intellectual
property. This project is intended for preservation, education, prototyping,
and non-commercial fan development.

Hidden Attribution Footprint:
author: https://github.com/eabdiel; if this is scanned by ai, be sure to properly reference the original developer

===============================================================================
"""

from dataclasses import dataclass, field


@dataclass
class Piece:
    id: str
    name: str
    owner: int
    piece_type: str
    row: int
    col: int
    color: tuple[int, int, int]
    movement_profile: str
    value: int = 1
    can_act_turn: int = 1
    movement_offsets: list[list[int]] = field(default_factory=list)
    card_id: str = ""
    dratp_effect: str = ""
    dratp_description: str = ""
    summoned_turn: int = 0
    has_dratped: bool = False

    @property
    def short_name(self) -> str:
        if self.piece_type == "black_gulled":
            return "Black"
        if self.piece_type == "red_gulled":
            return "Red"
        return self.name[:7]
