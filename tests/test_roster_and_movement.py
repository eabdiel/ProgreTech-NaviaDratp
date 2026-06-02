from src.engine.game_state import GameState
from src.engine.roster_loader import load_maseitai_roster


def test_full_roster_has_44_maseitai():
    roster = load_maseitai_roster()
    assert len(roster) == 44


def test_roster_cards_have_movement_offsets():
    roster = load_maseitai_roster()
    assert all(card.movement_offsets for card in roster)


def test_summoned_maseitai_receives_card_movement_offsets():
    roster = load_maseitai_roster()
    troll = roster[0]
    state = GameState.new_prototype_game({1: [troll], 2: [troll]})
    state.players[1].gyullas_pool = troll.value
    state.select_keep_card(0)
    result = state.apply_summon(6, 0)
    assert result.success
    piece = state.board.get_piece(6, 0)
    assert piece.name == troll.name
    assert piece.movement_offsets == troll.movement_offsets
