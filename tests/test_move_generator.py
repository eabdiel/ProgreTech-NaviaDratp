from src.engine.game_state import GameState


def test_gulled_has_forward_move():
    state = GameState.new_prototype_game()
    gulled = state.board.get_piece(5, 0)
    moves = state.get_legal_moves_for_piece(gulled)
    assert any(move.to_row == 4 and move.to_col == 0 for move in moves)
