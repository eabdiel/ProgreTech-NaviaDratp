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

from src.engine.game_state import GameState
from src.engine.roster_loader import load_maseitai_roster


def test_maseitai_cannot_dratp_until_more_than_one_turn_on_field():
    troll = load_maseitai_roster()[0]
    state = GameState.new_prototype_game({1: [troll], 2: [troll]})
    state.players[1].gyullas_pool = 99
    state.select_keep_card(0)
    state.apply_summon(6, 0)
    state.current_player = 1
    state.turn_number = 2
    result = state.apply_dratp(6, 0)
    assert not result.success


def test_laynard_dratp_gain_10_after_cost():
    laynard = [c for c in load_maseitai_roster() if c.id == "laynard"][0]
    state = GameState.new_prototype_game({1: [laynard], 2: [laynard]})
    state.players[1].gyullas_pool = 30
    state.select_keep_card(0)
    state.apply_summon(6, 0)
    state.current_player = 1
    state.turn_number = 5
    before = state.players[1].gyullas_pool
    result = state.apply_dratp(6, 0)
    assert result.success
    assert state.players[1].gyullas_pool == before
