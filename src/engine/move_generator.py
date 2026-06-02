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

from src.engine.coordinates import in_bounds
from src.engine.move import Move


# MoveGenerator produces legal move targets. Gulled have fixed rule-based movement; Maseitai movement comes from JSON offsets.
class MoveGenerator:
    KING_DELTAS = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

    def get_legal_moves(self, game_state, piece) -> list[Move]:
        if piece.can_act_turn > game_state.turn_number:
            return []
        if piece.piece_type == "black_gulled":
            return self._black_gulled_moves(game_state, piece)
        if piece.piece_type == "red_gulled":
            return self._red_gulled_moves(game_state, piece)
        if piece.piece_type == "maseitai" and piece.movement_offsets:
            return self._offset_moves(game_state, piece, piece.movement_offsets)
        return self._single_step_moves(game_state, piece, self.KING_DELTAS)

    def _single_step_moves(self, game_state, piece, deltas) -> list[Move]:
        moves = []
        for rd, cd in deltas:
            tr, tc = piece.row + rd, piece.col + cd
            if not in_bounds(tr, tc, game_state.board.size):
                continue
            target = game_state.board.get_piece(tr, tc)
            if target is None:
                moves.append(Move(piece.row, piece.col, tr, tc))
            elif target.owner != piece.owner:
                moves.append(Move(piece.row, piece.col, tr, tc, is_capture=True))
        return moves

    # Data-driven Maseitai movement. JSON offsets allow compass patterns to be tuned without rewriting engine code.
    def _offset_moves(self, game_state, piece, offsets) -> list[Move]:
        """Data-driven Maseitai movement.

        Offsets are stored from Player 1 perspective. For Player 2, row direction is flipped
        so the same data behaves correctly when viewed from the opposite side.
        """
        moves = []
        row_orientation = 1 if piece.owner == 1 else -1

        for raw_rd, raw_cd in offsets:
            rd = raw_rd * row_orientation
            cd = raw_cd
            tr, tc = piece.row + rd, piece.col + cd

            if not in_bounds(tr, tc, game_state.board.size):
                continue

            target = game_state.board.get_piece(tr, tc)
            if target is None:
                moves.append(Move(piece.row, piece.col, tr, tc))
            elif target.owner != piece.owner:
                moves.append(Move(piece.row, piece.col, tr, tc, is_capture=True))

        return moves

    def _black_gulled_moves(self, game_state, piece) -> list[Move]:
        direction = -1 if piece.owner == 1 else 1
        moves = []

        tr, tc = piece.row + direction, piece.col
        if in_bounds(tr, tc, game_state.board.size) and game_state.board.get_piece(tr, tc) is None:
            moves.append(Move(piece.row, piece.col, tr, tc))

        for cd in [-1, 1]:
            tr, tc = piece.row + direction, piece.col + cd
            if in_bounds(tr, tc, game_state.board.size):
                target = game_state.board.get_piece(tr, tc)
                if target is not None and target.owner != piece.owner:
                    moves.append(Move(piece.row, piece.col, tr, tc, is_capture=True))
        return moves

    def _red_gulled_moves(self, game_state, piece) -> list[Move]:
        direction = -1 if piece.owner == 1 else 1
        moves = []
        for cd in [-1, 0, 1]:
            tr, tc = piece.row + direction, piece.col + cd
            if not in_bounds(tr, tc, game_state.board.size):
                continue
            target = game_state.board.get_piece(tr, tc)
            if target is None:
                moves.append(Move(piece.row, piece.col, tr, tc))
            elif target.owner != piece.owner:
                moves.append(Move(piece.row, piece.col, tr, tc, is_capture=True))
        return moves
