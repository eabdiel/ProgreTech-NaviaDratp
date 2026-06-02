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
