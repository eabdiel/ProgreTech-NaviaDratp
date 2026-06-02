def in_bounds(row: int, col: int, board_size: int = 7) -> bool:
    return 0 <= row < board_size and 0 <= col < board_size
