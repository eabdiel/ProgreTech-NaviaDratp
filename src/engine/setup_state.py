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

from src.engine.roster_loader import load_maseitai_roster
from src.utils.constants import DRAFT_TARGET_COUNT, PLAYER_ONE, PLAYER_TWO


# SetupState handles the pre-game draft. Each player drafts from their own roster copy so both players may choose the same Maseitai type.
class SetupState:
    """Draft/setup phase state.

    Players alternate choosing Maseitai until each has DRAFT_TARGET_COUNT.
    Each player drafts from their own copy of the roster, so both players can choose Troll, etc.
    A single player cannot draft duplicate copies of the same Maseitai in this prototype.
    """

    def __init__(self) -> None:
        self.roster = load_maseitai_roster()
        self.drafts = {
            PLAYER_ONE: [],
            PLAYER_TWO: [],
        }
        self.current_player = PLAYER_ONE
        self.complete = False
        self.status_message = "Setup Phase: Player 1, choose your first Maseitai."

    def available_cards(self):
        own_drafted_ids = {card.id for card in self.drafts[self.current_player]}
        return [card for card in self.roster if card.id not in own_drafted_ids]

    def draft_card_by_available_index(self, index: int) -> bool:
        available = self.available_cards()
        if index < 0 or index >= len(available):
            self.status_message = "No card found there."
            return False

        if len(self.drafts[self.current_player]) >= DRAFT_TARGET_COUNT:
            self.status_message = f"Player {self.current_player} already has {DRAFT_TARGET_COUNT} Maseitai."
            return False

        card = available[index]
        self.drafts[self.current_player].append(card)
        self.status_message = f"Player {self.current_player} drafted {card.name}."

        if self.is_complete():
            self.complete = True
            self.status_message = "Setup complete. Starting match."
            return True

        self.current_player = PLAYER_TWO if self.current_player == PLAYER_ONE else PLAYER_ONE
        while len(self.drafts[self.current_player]) >= DRAFT_TARGET_COUNT and not self.is_complete():
            self.current_player = PLAYER_TWO if self.current_player == PLAYER_ONE else PLAYER_ONE

        if not self.is_complete():
            self.status_message += f" Player {self.current_player}, choose next."

        return True

    def is_complete(self) -> bool:
        return all(len(cards) >= DRAFT_TARGET_COUNT for cards in self.drafts.values())
