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
from src.engine.piece import Piece


class Board:
    def __init__(self, size: int = 7) -> None:
        self.size = size
        self.grid: list[list[Piece | None]] = [[None for _ in range(size)] for _ in range(size)]

    def place_piece(self, piece: Piece) -> None:
        if not in_bounds(piece.row, piece.col, self.size):
            raise ValueError(f"Piece position out of bounds: {piece}")
        if self.grid[piece.row][piece.col] is not None:
            raise ValueError(f"Square is already occupied: {piece.row},{piece.col}")
        self.grid[piece.row][piece.col] = piece

    def get_piece(self, row: int, col: int) -> Piece | None:
        if not in_bounds(row, col, self.size):
            return None
        return self.grid[row][col]

    def move_piece(self, from_row: int, from_col: int, to_row: int, to_col: int) -> Piece | None:
        piece = self.get_piece(from_row, from_col)
        if piece is None:
            raise ValueError("No piece exists at the source square.")
        captured = self.get_piece(to_row, to_col)
        self.grid[from_row][from_col] = None
        piece.row = to_row
        piece.col = to_col
        self.grid[to_row][to_col] = piece
        return captured

    def iter_pieces(self):
        for row in self.grid:
            for piece in row:
                if piece is not None:
                    yield piece
