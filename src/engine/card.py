from dataclasses import dataclass, field


@dataclass(frozen=True)
class MaseitaiCard:
    id: str
    name: str
    value: int
    description: str = ""
    navia_guard: bool = False
    number: int = 0
    movement_profile: str = "king"
    movement_offsets: list[list[int]] = field(default_factory=list)
    post_dratp_offsets: list[list[int]] = field(default_factory=list)
    dratp_effect: str = "generic_pulse"
    dratp_description: str = ""
