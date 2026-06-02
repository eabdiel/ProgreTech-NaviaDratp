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


@dataclass(frozen=True)
class MaseitaiCard:
    id: str
    name: str
    value: int
    description: str = ""
    navia_guard: bool = False
    number: int = 0
    movement_profile: str = "king"
    movement_offsets: list[list[int]] = field(default_factory=list)
    post_dratp_offsets: list[list[int]] = field(default_factory=list)
    dratp_effect: str = "generic_pulse"
    dratp_description: str = ""
