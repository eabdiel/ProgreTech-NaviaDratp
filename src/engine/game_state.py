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

from src.engine.board import Board
from src.engine.board_zones import BoardZones
from src.engine.card import MaseitaiCard
from src.engine.dratp_rules import DratpRules
from src.engine.gyullas import GyullasEconomy
from src.engine.move import Move
from src.engine.move_generator import MoveGenerator
from src.engine.move_result import MoveResult
from src.engine.piece import Piece
from src.engine.player import Player
from src.engine.roster_loader import load_maseitai_roster
from src.engine.win_conditions import WinConditions
from src.utils.constants import (
    BLACK_GULLED_COLOR, MASEITAI_P1_COLOR, MASEITAI_P2_COLOR,
    PLAYER_ONE, PLAYER_TWO, RED_GULLED_COLOR
)


# GameState is the core engine model. It owns the board, players, keeps, turn state, Gyullas, summoning, movement, captures, and Dratp routing.
class GameState:
    def __init__(self, board: Board, players: dict[int, Player], keeps: dict[int, list]) -> None:
        self.board = board
        self.players = players
        self.keeps = keeps
        self.current_player = PLAYER_ONE
        self.turn_number = 1
        self.move_generator = MoveGenerator()
        self.gyullas = GyullasEconomy()
        self.win_conditions = WinConditions()
        self.dratp_rules = DratpRules()
        self.captured_pieces = {PLAYER_ONE: [], PLAYER_TWO: []}
        self.winner = None
        self.pending_summon: tuple[int, object] | None = None
        self.status_message = "Player 1 starts. Move Gulled to earn Gyullas, then summon from the pool."

    # Builds the standard starting board. Gulled placement is fixed every match; Maseitai are provided by setup/draft or default roster.
    @classmethod
    def new_prototype_game(cls, drafted_keeps: dict[int, list] | None = None) -> "GameState":
        board = Board(size=7)
        players = {1: Player(1, "Player 1"), 2: Player(2, "Player 2")}

        if drafted_keeps is None:
            roster = load_maseitai_roster()
            drafted_keeps = {1: roster[:7], 2: roster[:7]}

        keeps = {1: list(drafted_keeps[1]), 2: list(drafted_keeps[2])}

        pieces = [
            Piece("p1_navia", "Estelle", 1, "navia", 6, 3, (230,230,255), "king", 0),
            Piece("p2_navia", "Debora", 2, "navia", 0, 3, (255,210,230), "king", 0),
            Piece("p1_red_l", "Red Gulled", 1, "red_gulled", 6, 1, RED_GULLED_COLOR, "red_gulled", 1),
            Piece("p1_red_r", "Red Gulled", 1, "red_gulled", 6, 5, RED_GULLED_COLOR, "red_gulled", 1),
            Piece("p2_red_l", "Red Gulled", 2, "red_gulled", 0, 1, RED_GULLED_COLOR, "red_gulled", 1),
            Piece("p2_red_r", "Red Gulled", 2, "red_gulled", 0, 5, RED_GULLED_COLOR, "red_gulled", 1),
        ]

        for col in range(7):
            pieces.append(Piece(f"p1_black_{col}", "Black Gulled", 1, "black_gulled", 5, col, BLACK_GULLED_COLOR, "black_gulled", 1))
            pieces.append(Piece(f"p2_black_{col}", "Black Gulled", 2, "black_gulled", 1, col, BLACK_GULLED_COLOR, "black_gulled", 1))

        for piece in pieces:
            board.place_piece(piece)

        return cls(board, players, keeps)

    def can_afford_card(self, owner: int, card_index: int) -> bool:
        if owner != self.current_player:
            return False
        if card_index < 0 or card_index >= len(self.keeps[owner]):
            return False
        card = self.keeps[owner][card_index]
        return self.players[owner].gyullas_pool >= card.value and bool(self.get_open_summon_squares(owner))

    def select_keep_card(self, card_index: int) -> MoveResult:
        owner = self.current_player
        if card_index < 0 or card_index >= len(self.keeps[owner]):
            return MoveResult(False, "No card found there.")
        card = self.keeps[owner][card_index]
        if not self.get_open_summon_squares(owner):
            return MoveResult(False, "No open summon squares.")
        if self.players[owner].gyullas_pool < card.value:
            return MoveResult(False, f"Not enough Gyullas to summon {card.name}. Need {card.value}G.")
        self.pending_summon = (card_index, card)
        return MoveResult(True, f"Summoning {card.name}. Choose a yellow-icon summon square.")

    def get_open_summon_squares(self, owner: int | None = None) -> list[tuple[int, int]]:
        owner = owner or self.current_player
        return [(r, c) for r, c in self.get_summon_squares(owner) if self.board.get_piece(r, c) is None]

    def get_summon_squares(self, owner: int) -> list[tuple[int, int]]:
        return list(BoardZones.SUMMON_SQUARES[owner])

    # Summoning spends Gyullas, removes the card from the player's Keep, and creates a battlefield Maseitai piece.
    def apply_summon(self, row: int, col: int) -> MoveResult:
        if self.pending_summon is None:
            return MoveResult(False, "No Maseitai selected.")
        if (row, col) not in self.get_open_summon_squares():
            return MoveResult(False, "That summon square is not open.")
        card_index, card = self.pending_summon
        player = self.players[self.current_player]
        cost = card.value
        if player.gyullas_pool < cost:
            self.pending_summon = None
            return MoveResult(False, f"Not enough Gyullas. {card.name} costs {cost}G.")
        player.gyullas_pool -= cost
        self.keeps[self.current_player].pop(card_index)
        piece = Piece(
            id=f"p{self.current_player}_{card.id}_{self.turn_number}",
            name=card.name,
            owner=self.current_player,
            piece_type="maseitai",
            row=row,
            col=col,
            color=MASEITAI_P1_COLOR if self.current_player == 1 else MASEITAI_P2_COLOR,
            movement_profile=card.movement_profile,
            value=card.value,
            can_act_turn=self.turn_number + 2,
            movement_offsets=card.movement_offsets,
            card_id=card.id,
            dratp_effect=card.dratp_effect,
            dratp_description=card.dratp_description,
            summoned_turn=self.turn_number,
        )
        self.board.place_piece(piece)
        self.pending_summon = None
        self._next_turn()
        return MoveResult(True, f"Summoned {card.name} for {cost}G.")

    def get_legal_moves_for_piece(self, piece: Piece) -> list[Move]:
        if piece.owner != self.current_player:
            return []
        return self.move_generator.get_legal_moves(self, piece)

    # Applies a legal move, awards Gyullas for Gulled movement, handles captures, checks victory, and advances the turn.
    def apply_move(self, move: Move) -> MoveResult:
        if self.winner is not None:
            return MoveResult(False, f"Player {self.winner} already won. Press R to reset.")
        piece = self.board.get_piece(move.from_row, move.from_col)
        if piece is None:
            return MoveResult(False, "No piece found at the selected square.")
        if piece.owner != self.current_player:
            return MoveResult(False, "That is not your piece.")
        legal = self.get_legal_moves_for_piece(piece)
        if not any(m.to_row == move.to_row and m.to_col == move.to_col for m in legal):
            return MoveResult(False, "Illegal move.")
        current = self.players[self.current_player]
        captured = self.board.move_piece(move.from_row, move.from_col, move.to_row, move.to_col)
        parts = [f"Player {self.current_player} moved {piece.name}."]
        reward = self.gyullas.award_for_move(current, piece)
        if reward:
            parts.append(f"+{reward}G.")
        if captured:
            self.captured_pieces[self.current_player].append(captured)
            cap_reward = self.gyullas.award_for_capture(current, captured)
            parts.append(f"Captured {captured.name}" + (f" for +{cap_reward}G." if cap_reward else "."))
        winner = self.win_conditions.check_winner(self)
        if winner:
            self.winner = winner
            return MoveResult(True, f"Player {winner} wins by capturing the opposing Navia!")
        self._next_turn()
        return MoveResult(True, " ".join(parts))

    # Dratp calls are routed to DratpRules so special abilities stay modular and can grow independently.
    def apply_dratp(self, row: int, col: int) -> MoveResult:
        piece = self.board.get_piece(row, col)
        return self.dratp_rules.apply(self, piece)

    def send_piece_to_graveyard(self, piece: Piece) -> None:
        if self.board.get_piece(piece.row, piece.col) is piece:
            self.board.grid[piece.row][piece.col] = None
        self.captured_pieces[2 if piece.owner == 1 else 1].append(piece)

    def return_piece_to_keep(self, piece: Piece) -> None:
        if self.board.get_piece(piece.row, piece.col) is piece:
            self.board.grid[piece.row][piece.col] = None
        self.keeps[piece.owner].append(MaseitaiCard(
            id=piece.card_id or piece.name.lower().replace(" ", "_"),
            name=piece.name,
            value=piece.value,
            movement_profile=piece.movement_profile,
            movement_offsets=piece.movement_offsets,
            dratp_effect=piece.dratp_effect,
            dratp_description=piece.dratp_description,
        ))

    def move_all_black_gulled_forward(self, owner: int) -> int:
        direction = -1 if owner == 1 else 1
        moved = 0
        pieces = [p for p in self.board.iter_pieces() if p.owner == owner and p.piece_type == "black_gulled"]
        pieces.sort(key=lambda p: p.row, reverse=(owner == 1))
        for piece in pieces:
            target_row = piece.row + direction
            target_col = piece.col
            if 0 <= target_row < self.board.size and self.board.get_piece(target_row, target_col) is None:
                self.board.move_piece(piece.row, piece.col, target_row, target_col)
                moved += 1
        return moved

    def graveyard_label(self, owner: int) -> str:
        items = self.captured_pieces[owner]
        return "No pieces" if not items else ", ".join(piece.name for piece in items[-8:])

    def keep_label(self, owner: int) -> str:
        cards = self.keeps[owner]
        return "No pieces" if not cards else ", ".join(card.name for card in cards[:8])

    def _next_turn(self) -> None:
        self.current_player = 2 if self.current_player == 1 else 1
        self.turn_number += 1
