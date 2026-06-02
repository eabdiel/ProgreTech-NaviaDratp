import math

from src.engine.board_zones import BoardZones


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
