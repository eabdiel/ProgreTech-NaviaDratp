from src.engine.board_zones import BoardZones
from src.engine.game_state import GameState
from src.engine.move import Move


def test_default_setup_has_red_and_black_gulled():
    state = GameState.new_prototype_game()
    pieces = list(state.board.iter_pieces())
    assert len(pieces) == 20
    assert len([p for p in pieces if p.piece_type == "red_gulled"]) == 4
    assert len([p for p in pieces if p.piece_type == "black_gulled"]) == 14


def test_correct_summon_squares_for_player_one():
    state = GameState.new_prototype_game()
    expected = {(6,0), (6,1), (6,2), (6,4), (6,5), (6,6), (5,0), (5,6)}
    assert set(state.get_summon_squares(1)) == expected


def test_correct_summon_squares_for_player_two():
    state = GameState.new_prototype_game()
    expected = {(0,0), (0,1), (0,2), (0,4), (0,5), (0,6), (1,0), (1,6)}
    assert set(state.get_summon_squares(2)) == expected


def test_starting_game_only_four_open_summon_spaces_per_player():
    state = GameState.new_prototype_game()
    assert len(state.get_open_summon_squares(1)) == 4
    assert len(state.get_open_summon_squares(2)) == 4


def test_gyullas_reduction_zone_is_middle_row_five_squares():
    assert set(BoardZones.GRZ_SQUARES) == {(3,1), (3,2), (3,3), (3,4), (3,5)}


def test_black_gulled_move_awards_one_gyullas():
    state = GameState.new_prototype_game()
    result = state.apply_move(Move(5, 0, 4, 0))
    assert result.success
    assert state.players[1].gyullas_pool == 1


def test_red_gulled_move_awards_three_gyullas_when_target_is_open():
    state = GameState.new_prototype_game()
    state.board.grid[5][2] = None
    result = state.apply_move(Move(6, 1, 5, 2))
    assert result.success
    assert state.players[1].gyullas_pool == 3


def test_red_gulled_is_initially_blocked_by_starting_black_gulled_wall():
    state = GameState.new_prototype_game()
    red = state.board.get_piece(6, 1)
    assert state.get_legal_moves_for_piece(red) == []
