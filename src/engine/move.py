from dataclasses import dataclass


@dataclass(frozen=True)
class Move:
    from_row: int
    from_col: int
    to_row: int
    to_col: int
    is_capture: bool = False
