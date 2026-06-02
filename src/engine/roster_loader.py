from src.engine.card import MaseitaiCard
from src.utils.constants import DATA_DIR
from src.utils.json_loader import load_json


def load_maseitai_roster() -> list[MaseitaiCard]:
    raw_cards = load_json(DATA_DIR / "maseitai_roster.json")
    return [
        MaseitaiCard(
            id=item["id"],
            name=item["name"],
            value=int(item["value"]),
            description=item.get("description", ""),
            navia_guard=bool(item.get("navia_guard", False)),
            number=int(item.get("number", 0)),
            movement_profile=item.get("movement_profile", "king"),
            movement_offsets=item.get("movement_offsets", []),
            post_dratp_offsets=item.get("post_dratp_offsets", []),
            dratp_effect=item.get("dratp_effect", "generic_pulse"),
            dratp_description=item.get("dratp_description", item.get("description", "")),
        )
        for item in raw_cards
    ]
