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

class WinConditions:
    def check_winner(self, game_state):
        p1 = p2 = False
        for piece in game_state.board.iter_pieces():
            if piece.piece_type == "navia" and piece.owner == 1:
                p1 = True
            if piece.piece_type == "navia" and piece.owner == 2:
                p2 = True
        if not p1:
            return 2
        if not p2:
            return 1
        return None
