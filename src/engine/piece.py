from dataclasses import dataclass, field


@dataclass
class Piece:
    id: str
    name: str
    owner: int
    piece_type: str
    row: int
    col: int
    color: tuple[int, int, int]
    movement_profile: str
    value: int = 1
    can_act_turn: int = 1
    movement_offsets: list[list[int]] = field(default_factory=list)
    card_id: str = ""
    dratp_effect: str = ""
    dratp_description: str = ""
    summoned_turn: int = 0
    has_dratped: bool = False

    @property
    def short_name(self) -> str:
        if self.piece_type == "black_gulled":
            return "Black"
        if self.piece_type == "red_gulled":
            return "Red"
        return self.name[:7]
