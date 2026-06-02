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

# BoardZones keeps fixed board-coordinate rules in one place: summon squares, Navia squares, and the Gyullas Reduction Zone.
class BoardZones:
    """Shared board-zone definitions.

    Coordinates are row, col.
    """

    SUMMON_SQUARES = {
        1: [(6, 0), (6, 1), (6, 2), (6, 4), (6, 5), (6, 6), (5, 0), (5, 6)],
        2: [(0, 0), (0, 1), (0, 2), (0, 4), (0, 5), (0, 6), (1, 0), (1, 6)],
    }

    GRZ_SQUARES = [(3, 1), (3, 2), (3, 3), (3, 4), (3, 5)]

    NAVIA_SQUARES = {
        1: (6, 3),
        2: (0, 3),
    }
