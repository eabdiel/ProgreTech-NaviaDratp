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

from src.engine.move_result import MoveResult


# DratpRules owns active Maseitai ability execution and cost validation. Complex effects can be added one ability at a time.
class DratpRules:
    # Eligibility check: only current player's Maseitai, only after field age > 1 turn, and only if the player can pay the adjusted cost.
    def can_dratp(self, game_state, piece) -> tuple[bool, str]:
        if piece is None:
            return False, "No piece selected."
        if piece.piece_type != "maseitai":
            return False, "Only Maseitai can Dratp."
        if piece.owner != game_state.current_player:
            return False, "That is not your piece."
        if game_state.turn_number <= piece.summoned_turn + 1:
            return False, "This Maseitai must be on the field for more than 1 turn before Dratp."
        cost = game_state.gyullas.dratp_cost(piece.value, piece.row, piece.col)
        if game_state.players[piece.owner].gyullas_pool < cost:
            return False, f"Not enough Gyullas. Dratp cost is {cost}G."
        return True, "Dratp available."

    # Applies the first-pass Dratp effect, updates Gyullas/pieces as needed, flags the piece, and passes the turn.
    def apply(self, game_state, piece) -> MoveResult:
        can_use, reason = self.can_dratp(game_state, piece)
        if not can_use:
            return MoveResult(False, reason)

        player = game_state.players[piece.owner]
        opponent_id = 2 if piece.owner == 1 else 1
        opponent = game_state.players[opponent_id]
        cost = game_state.gyullas.dratp_cost(piece.value, piece.row, piece.col)
        player.gyullas_pool -= cost

        effect = piece.dratp_effect or "generic_pulse"
        msg = f"{piece.name} Dratp activated for {cost}G."

        if effect == "gain_gyullas_1":
            player.gyullas_pool += 1
            msg += " +1G gained."
        elif effect == "gain_gyullas_6":
            player.gyullas_pool += 6
            msg += " +6G gained."
        elif effect == "gain_gyullas_10":
            player.gyullas_pool += 10
            msg += " +10G gained."
        elif effect == "opponent_lose_4":
            lost = min(4, opponent.gyullas_pool)
            opponent.gyullas_pool -= lost
            msg += f" Opponent lost {lost}G."
        elif effect == "opponent_lose_15_self_grave":
            lost = min(15, opponent.gyullas_pool)
            opponent.gyullas_pool -= lost
            game_state.send_piece_to_graveyard(piece)
            msg += f" Opponent lost {lost}G. {piece.name} went to Graveyard."
        elif effect == "gain_graveyard_count":
            count = len(game_state.captured_pieces[1]) + len(game_state.captured_pieces[2])
            player.gyullas_pool += count
            msg += f" +{count}G from graveyard count."
        elif effect == "return_self_to_keep":
            game_state.return_piece_to_keep(piece)
            msg += f" {piece.name} returned to Keep."
        elif effect == "move_black_gulled_up":
            moved = game_state.move_all_black_gulled_forward(piece.owner)
            msg += f" {moved} Black Gulled moved forward."
        elif effect.startswith("passive"):
            msg += " This is a passive effect; no active change was applied."
        else:
            msg += f" Effect placeholder: {piece.dratp_description or effect}."

        piece.has_dratped = True
        if game_state.winner is None:
            game_state._next_turn()
        return MoveResult(True, msg)
