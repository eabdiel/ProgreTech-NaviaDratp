class WinConditions:
    def check_winner(self, game_state):
        p1 = p2 = False
        for piece in game_state.board.iter_pieces():
            if piece.piece_type == "navia" and piece.owner == 1:
                p1 = True
            if piece.piece_type == "navia" and piece.owner == 2:
                p2 = True
        if not p1:
            return 2
        if not p2:
            return 1
        return None
