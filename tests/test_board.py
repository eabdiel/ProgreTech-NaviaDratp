from src.engine.board import Board
from src.engine.piece import Piece


def test_board_is_7_by_7_by_default():
    board = Board()
    assert board.size == 7
    assert len(board.grid) == 7
    assert len(board.grid[0]) == 7


def test_place_piece():
    board = Board()
    piece = Piece("x", "Test", 1, "test", 3, 3, (255, 255, 255), "king")
    board.place_piece(piece)
    assert board.get_piece(3, 3) == piece
