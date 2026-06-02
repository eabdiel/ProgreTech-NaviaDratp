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

import math

from src.engine.board_zones import BoardZones


# GyullasEconomy centralizes point/currency rules so rewards and Dratp-cost reductions are not scattered across the UI.
class GyullasEconomy:
    BLACK_GULLED_MOVE_REWARD = 1
    RED_GULLED_MOVE_REWARD = 3

    def award_for_move(self, player, piece) -> int:
        if piece.piece_type == "black_gulled":
            player.gyullas_pool += self.BLACK_GULLED_MOVE_REWARD
            return self.BLACK_GULLED_MOVE_REWARD
        if piece.piece_type == "red_gulled":
            player.gyullas_pool += self.RED_GULLED_MOVE_REWARD
            return self.RED_GULLED_MOVE_REWARD
        return 0

    def award_for_capture(self, player, captured_piece) -> int:
        if captured_piece.piece_type == "navia":
            return 0
        amount = captured_piece.value
        player.gyullas_pool += amount
        return amount

    def reduced_cost(self, base_cost: int) -> int:
        return max(1, math.ceil(base_cost / 2))

    def dratp_cost(self, base_cost: int, row: int, col: int) -> int:
        if (row, col) in BoardZones.GRZ_SQUARES:
            return self.reduced_cost(base_cost)
        return base_cost

    def summon_cost(self, card, row: int, col: int) -> int:
        return card.value
