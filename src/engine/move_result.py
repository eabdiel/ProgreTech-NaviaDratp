from dataclasses import dataclass


@dataclass
class MoveResult:
    success: bool
    message: str
