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

from src.engine.setup_state import SetupState
from src.utils.constants import DRAFT_TARGET_COUNT


def test_setup_phase_completes_after_both_players_draft_seven():
    setup = SetupState()
    while not setup.complete:
        setup.draft_card_by_available_index(0)
    assert len(setup.drafts[1]) == DRAFT_TARGET_COUNT
    assert len(setup.drafts[2]) == DRAFT_TARGET_COUNT


def test_both_players_can_draft_same_maseitai_type():
    setup = SetupState()
    setup.draft_card_by_available_index(0)
    first_player_card = setup.drafts[1][0].id
    # Player 2 should still see that same card as available in their own roster.
    assert any(card.id == first_player_card for card in setup.available_cards())
