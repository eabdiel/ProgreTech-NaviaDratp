import pygame

from src.engine.game_state import GameState
from src.engine.move import Move
from src.engine.setup_state import SetupState
from src.ui.board_view import BoardView
from src.ui.hud import HUD
from src.ui.setup_view import SetupView
from src.utils.constants import COLOR_BACKGROUND


class GameApp:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.mode = "setup"
        self.setup_state = SetupState()
        self.game_state = None
        self.board_view = BoardView()
        self.setup_view = SetupView()
        self.hud = HUD()
        self.context_menu_pos = None
        self.context_menu_square = None

    def reset_to_setup(self) -> None:
        self.mode = "setup"
        self.setup_state = SetupState()
        self.game_state = None
        self.board_view.clear_selection()
        self.context_menu_pos = None
        self.context_menu_square = None

    def start_match_from_setup(self) -> None:
        self.game_state = GameState.new_prototype_game(self.setup_state.drafts)
        self.mode = "game"
        self.board_view.clear_selection()
        self.context_menu_pos = None
        self.context_menu_square = None

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back_to_menu"
            if event.key == pygame.K_r:
                self.reset_to_setup()
                return None

        if self.mode == "setup":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                index = self.setup_view.card_at(event.pos, self.setup_state)
                if index is not None:
                    self.setup_state.draft_card_by_available_index(index)
                    if self.setup_state.complete:
                        self.start_match_from_setup()
            return None

        if self.game_state is None:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            board_pos = self.board_view.pixel_to_board(event.pos)
            if board_pos:
                piece = self.game_state.board.get_piece(*board_pos)
                if piece and piece.owner == self.game_state.current_player and piece.piece_type == "maseitai":
                    self.context_menu_pos = event.pos
                    self.context_menu_square = board_pos
                    self.board_view.selected_info_square = board_pos
                    self.game_state.status_message = f"Right-click menu opened for {piece.name}."
                else:
                    self.context_menu_pos = None
                    self.context_menu_square = None
            return None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.context_menu_pos and self.context_menu_square:
                action = self.board_view.context_menu_at(event.pos)
                if action == "dratp":
                    row, col = self.context_menu_square
                    result = self.game_state.apply_dratp(row, col)
                    self.game_state.status_message = result.message
                    self.board_view.clear_selection()
                    self.context_menu_pos = None
                    self.context_menu_square = None
                    return None
                self.context_menu_pos = None
                self.context_menu_square = None

            if self._handle_keep_click(event.pos):
                return None

            board_pos = self.board_view.pixel_to_board(event.pos)
            if board_pos:
                self._handle_board_click(*board_pos)

        return None

    def _handle_keep_click(self, pos: tuple[int, int]) -> bool:
        clicked_card_index = self.board_view.keep_card_at(pos, self.game_state.current_player)
        if clicked_card_index is None:
            return False
        result = self.game_state.select_keep_card(clicked_card_index)
        if result.success:
            self.board_view.set_summon_selection(self.game_state.get_open_summon_squares())
        else:
            self.board_view.clear_selection()
        self.game_state.status_message = result.message
        return True

    def _handle_board_click(self, row: int, col: int) -> None:
        if self.game_state.winner is not None:
            self.game_state.status_message = f"Player {self.game_state.winner} already won. Press R to reset."
            return

        if self.game_state.pending_summon is not None:
            result = self.game_state.apply_summon(row, col)
            self.board_view.clear_selection()
            self.game_state.status_message = result.message
            return

        selected = self.board_view.selected_square
        if selected is None:
            piece = self.game_state.board.get_piece(row, col)
            if piece and piece.owner == self.game_state.current_player:
                legal_moves = self.game_state.get_legal_moves_for_piece(piece)
                self.board_view.set_piece_selection((row, col), legal_moves)
                self.game_state.status_message = f"Selected {piece.name}. Choose a highlighted square."
            return

        if (row, col) == selected:
            self.board_view.clear_selection()
            self.game_state.status_message = "Selection cleared."
            return

        if (row, col) in self.board_view.legal_move_targets:
            move = Move(selected[0], selected[1], row, col)
            result = self.game_state.apply_move(move)
            self.board_view.clear_selection()
            self.game_state.status_message = result.message
            return

        piece = self.game_state.board.get_piece(row, col)
        if piece and piece.owner == self.game_state.current_player:
            legal_moves = self.game_state.get_legal_moves_for_piece(piece)
            self.board_view.set_piece_selection((row, col), legal_moves)
            self.game_state.status_message = f"Selected {piece.name}. Choose a highlighted square."
        else:
            self.board_view.clear_selection()
            self.game_state.status_message = "Invalid target."

    def draw(self) -> None:
        self.screen.fill(COLOR_BACKGROUND)
        if self.mode == "setup":
            self.setup_view.draw(self.screen, self.setup_state)
        elif self.game_state is not None:
            self.board_view.draw(self.screen, self.game_state)
            if self.context_menu_pos and self.context_menu_square:
                piece = self.game_state.board.get_piece(*self.context_menu_square)
                if piece:
                    self.board_view.show_context_menu(self.screen, self.context_menu_pos, piece)
            self.hud.draw(self.screen, self.game_state)
