import pygame

from src.engine.board_zones import BoardZones
from src.utils.constants import (
    BOARD_ORIGIN_X, BOARD_ORIGIN_Y, BOARD_SIZE, TILE_SIZE,
    COLOR_ACCENT, COLOR_BACKGROUND, COLOR_WARNING, COLOR_SUCCESS, COLOR_BOARD_DARK, COLOR_BOARD_GRID, COLOR_BOARD_LIGHT,
    COLOR_CAPTURE, COLOR_ERROR, COLOR_GRZ_OUTLINE, COLOR_LEGAL_MOVE, COLOR_MUTED_TEXT,
    COLOR_NAVIA_MARK, COLOR_PANEL, COLOR_PANEL_DARK, COLOR_SELECTED,
    COLOR_SUMMON_OUTLINE, COLOR_TEXT, PLAYER_COLORS
)


class BoardView:
    def __init__(self) -> None:
        self.board_size = BOARD_SIZE
        self.tile_size = TILE_SIZE
        self.origin_x = BOARD_ORIGIN_X
        self.origin_y = BOARD_ORIGIN_Y
        self.selected_square = None
        self.legal_move_targets = set()
        self.capture_targets = set()
        self.summon_targets = set()
        self.context_menu_rect = None
        self.selected_info_square = None

        self.summon_squares = set(BoardZones.SUMMON_SQUARES[1] + BoardZones.SUMMON_SQUARES[2])
        self.grz_squares = set(BoardZones.GRZ_SQUARES)

        self.piece_font = pygame.font.SysFont("arial", 12, bold=True)
        self.coord_font = pygame.font.SysFont("arial", 16, bold=True)
        self.small_font = pygame.font.SysFont("arial", 13)
        self.tiny_font = pygame.font.SysFont("arial", 11)
        self.title_font = pygame.font.SysFont("georgia", 34, bold=True)
        self.section_font = pygame.font.SysFont("georgia", 22, bold=True)

    def set_piece_selection(self, square, legal_moves) -> None:
        self.selected_square = square
        self.selected_info_square = square
        self.summon_targets.clear()
        self.legal_move_targets = {(move.to_row, move.to_col) for move in legal_moves}
        self.capture_targets = {(move.to_row, move.to_col) for move in legal_moves if move.is_capture}

    def set_summon_selection(self, summon_targets) -> None:
        self.selected_square = None
        self.legal_move_targets.clear()
        self.capture_targets.clear()
        self.summon_targets = set(summon_targets)

    def clear_selection(self) -> None:
        self.selected_square = None
        self.legal_move_targets.clear()
        self.capture_targets.clear()
        self.summon_targets.clear()

    def keep_card_at(self, pos, owner):
        for index, rect in self._keep_card_rects(owner):
            if rect.collidepoint(pos):
                return index
        return None

    def _keep_card_rects(self, owner):
        y = 862 if owner == 1 else 34
        start_x = self.origin_x
        width = 72
        gap = 10
        return [(i, pygame.Rect(start_x + i * (width + gap), y, width, 84)) for i in range(7)]

    def pixel_to_board(self, pos):
        x, y = pos
        if not (self.origin_x <= x < self.origin_x + self.board_size * self.tile_size and self.origin_y <= y < self.origin_y + self.board_size * self.tile_size):
            return None
        return int((y - self.origin_y) // self.tile_size), int((x - self.origin_x) // self.tile_size)

    def draw(self, screen, game_state) -> None:
        self._draw_left_panel(screen, game_state)
        self._draw_right_panels(screen)
        self._draw_board(screen)
        self._draw_pieces(screen, game_state)
        self._draw_keep_cards(screen, game_state)
        self._draw_selected_piece_panel(screen, game_state)
        self._draw_labels(screen)

    def _draw_labels(self, screen) -> None:
        for col in range(7):
            x = self.origin_x + col * self.tile_size + self.tile_size // 2
            label = self.coord_font.render(str(col), True, COLOR_ACCENT)
            screen.blit(label, label.get_rect(center=(x, self.origin_y - 22)))
        for row in range(7):
            y = self.origin_y + row * self.tile_size + self.tile_size // 2
            label = self.coord_font.render(str(row), True, COLOR_ACCENT)
            screen.blit(label, label.get_rect(center=(self.origin_x - 22, y)))

    def _draw_left_panel(self, screen, game_state) -> None:
        panel = pygame.Rect(16, 16, 300, 912)
        pygame.draw.rect(screen, COLOR_PANEL_DARK, panel, border_radius=10)
        pygame.draw.rect(screen, COLOR_BOARD_GRID, panel, width=2, border_radius=10)

        title = self.title_font.render("NAVIA", True, COLOR_ACCENT)
        title2 = self.title_font.render("DRATP", True, COLOR_ACCENT)
        screen.blit(title, title.get_rect(center=(166, 58)))
        screen.blit(title2, title2.get_rect(center=(166, 98)))

        turn_panel = pygame.Rect(32, 140, 268, 86)
        pygame.draw.rect(screen, COLOR_PANEL, turn_panel, border_radius=8)
        pygame.draw.rect(screen, COLOR_BOARD_GRID, turn_panel, width=1, border_radius=8)
        screen.blit(self.section_font.render(f"TURN {game_state.turn_number}", True, COLOR_ACCENT), (106, 158))
        screen.blit(self.small_font.render(f"Player {game_state.current_player}", True, COLOR_TEXT), (122, 195))

        y = 244
        for owner, label in [(1, "P1 GYULLAS"), (2, "P2 GYULLAS")]:
            box = pygame.Rect(32, y, 268, 80)
            pygame.draw.rect(screen, COLOR_PANEL, box, border_radius=8)
            pygame.draw.rect(screen, PLAYER_COLORS[owner], box, width=1, border_radius=8)
            screen.blit(self.small_font.render(label, True, PLAYER_COLORS[owner]), (82, y + 16))
            screen.blit(self.section_font.render(str(game_state.players[owner].gyullas_pool), True, COLOR_TEXT), (82, y + 38))
            pygame.draw.circle(screen, PLAYER_COLORS[owner], (58, y + 40), 20)
            pygame.draw.circle(screen, COLOR_TEXT, (58, y + 40), 20, width=1)
            y += 92

        self._draw_side_list(screen, pygame.Rect(32, 454, 268, 154), "KEEP", game_state.keep_label(game_state.current_player))
        self._draw_side_list(screen, pygame.Rect(32, 628, 268, 154), "GRAVEYARD", game_state.graveyard_label(game_state.current_player))

    def _draw_side_list(self, screen, rect, title, text) -> None:
        pygame.draw.rect(screen, COLOR_PANEL, rect, border_radius=8)
        pygame.draw.rect(screen, COLOR_BOARD_GRID, rect, width=1, border_radius=8)
        title_surface = self.section_font.render(title, True, COLOR_ACCENT)
        title_rect = title_surface.get_rect(center=(rect.centerx, rect.y + 24))
        screen.blit(title_surface, title_rect)
        self._draw_wrapped(screen, text, rect.x + 18, rect.y + 64, rect.width - 36, COLOR_TEXT)

    def _draw_right_panels(self, screen) -> None:
        legend = pygame.Rect(1260, 16, 284, 264)
        pygame.draw.rect(screen, COLOR_PANEL_DARK, legend, border_radius=10)
        pygame.draw.rect(screen, COLOR_BOARD_GRID, legend, width=2, border_radius=10)
        screen.blit(self.section_font.render("BOARD LEGEND", True, COLOR_ACCENT), (1304, 42))

        pygame.draw.rect(screen, COLOR_BACKGROUND, pygame.Rect(1280, 86, 38, 38))
        pygame.draw.rect(screen, COLOR_SUMMON_OUTLINE, pygame.Rect(1280, 86, 38, 38), width=4)
        self._draw_summon_icon(screen, pygame.Rect(1280, 86, 38, 38))
        screen.blit(self.small_font.render("SUMMONING SPACES", True, COLOR_ACCENT), (1332, 86))
        self._draw_wrapped(screen, "Only open summon squares may receive Maseitai.", 1332, 108, 180, COLOR_TEXT)

        pygame.draw.rect(screen, COLOR_BACKGROUND, pygame.Rect(1280, 178, 38, 38))
        pygame.draw.rect(screen, COLOR_GRZ_OUTLINE, pygame.Rect(1280, 178, 38, 38), width=4)
        screen.blit(self.small_font.render("GYULLAS REDUCTION ZONE", True, COLOR_ERROR), (1332, 176))
        self._draw_wrapped(screen, "Dratp cost is reduced by half, rounded up.", 1332, 198, 180, COLOR_TEXT)

        overview = pygame.Rect(1260, 296, 284, 280)
        pygame.draw.rect(screen, COLOR_PANEL_DARK, overview, border_radius=10)
        pygame.draw.rect(screen, COLOR_BOARD_GRID, overview, width=2, border_radius=10)
        screen.blit(self.section_font.render("TURN OVERVIEW", True, COLOR_ACCENT), (1302, 322))
        bullets = [
            "Move one battlefield piece.",
            "OR summon one Maseitai from your pool.",
            "Earn Gyullas by moving Gulled.",
            "Capture the opposing Navia to win.",
        ]
        y = 372
        for bullet in bullets:
            self._draw_wrapped(screen, f"- {bullet}", 1286, y, 230, COLOR_TEXT)
            y += 50

    def _draw_board(self, screen) -> None:
        border = pygame.Rect(self.origin_x - 8, self.origin_y - 8, self.board_size * self.tile_size + 16, self.board_size * self.tile_size + 16)
        pygame.draw.rect(screen, COLOR_BOARD_GRID, border, border_radius=5)

        for row in range(7):
            for col in range(7):
                rect = pygame.Rect(self.origin_x + col * self.tile_size, self.origin_y + row * self.tile_size, self.tile_size, self.tile_size)
                color = COLOR_BOARD_LIGHT if (row + col) % 2 == 0 else COLOR_BOARD_DARK
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, COLOR_BOARD_GRID, rect, width=1)

                if (row, col) in [(0, 3), (6, 3)]:
                    pygame.draw.circle(screen, COLOR_NAVIA_MARK, rect.center, 24)
                    pygame.draw.circle(screen, COLOR_ACCENT, rect.center, 24, width=2)

                if (row, col) in self.summon_squares:
                    pygame.draw.rect(screen, COLOR_SUMMON_OUTLINE, rect.inflate(-4, -4), width=4)
                    self._draw_summon_icon(screen, rect)

                if (row, col) in self.grz_squares:
                    pygame.draw.rect(screen, COLOR_GRZ_OUTLINE, rect.inflate(-12, -12), width=4)

                if self.selected_square == (row, col):
                    pygame.draw.rect(screen, COLOR_SELECTED, rect.inflate(-2, -2), width=5)

                if (row, col) in self.legal_move_targets:
                    pygame.draw.circle(screen, COLOR_CAPTURE if (row, col) in self.capture_targets else COLOR_LEGAL_MOVE, rect.center, 12)

                if (row, col) in self.summon_targets:
                    pygame.draw.circle(screen, COLOR_SUMMON_OUTLINE, rect.center, 18, width=5)

    def _draw_summon_icon(self, screen, rect) -> None:
        center = rect.center
        size = min(rect.width, rect.height) // 5
        points = [
            (center[0], center[1] - size),
            (center[0] + size, center[1]),
            (center[0], center[1] + size),
            (center[0] - size, center[1]),
        ]
        pygame.draw.polygon(screen, COLOR_ACCENT, points)
        pygame.draw.circle(screen, COLOR_PANEL_DARK, center, max(2, size // 3))

    def _draw_pieces(self, screen, game_state) -> None:
        for piece in game_state.board.iter_pieces():
            x = self.origin_x + piece.col * self.tile_size
            y = self.origin_y + piece.row * self.tile_size
            rect = pygame.Rect(x + 9, y + 10, self.tile_size - 18, self.tile_size - 18)
            pygame.draw.ellipse(screen, piece.color, rect)
            pygame.draw.ellipse(screen, PLAYER_COLORS[piece.owner], rect, width=3)

            fg = COLOR_TEXT if piece.piece_type in ("black_gulled", "red_gulled") else (18, 16, 13)
            name_surf = self.piece_font.render(piece.short_name, True, fg)
            value_surf = self.tiny_font.render(f"{piece.value}G", True, fg)
            screen.blit(name_surf, name_surf.get_rect(center=(rect.centerx, rect.centery - 6)))
            screen.blit(value_surf, value_surf.get_rect(center=(rect.centerx, rect.centery + 12)))

            if getattr(piece, "has_dratped", False):
                flag_rect = pygame.Rect(rect.right - 20, rect.top - 2, 24, 16)
                pygame.draw.rect(screen, COLOR_ACCENT, flag_rect, border_radius=3)
                pygame.draw.rect(screen, COLOR_PANEL_DARK, flag_rect, width=1, border_radius=3)
                flag_text = self.tiny_font.render("D", True, COLOR_PANEL_DARK)
                screen.blit(flag_text, flag_text.get_rect(center=flag_rect.center))

    def _draw_keep_cards(self, screen, game_state) -> None:
        for owner in [2, 1]:
            label_y = 12 if owner == 2 else 826
            y = 34 if owner == 2 else 862
            cards = game_state.keeps[owner]
            title = "OPPONENT POOL" if owner != game_state.current_player else "SUMMONING POOL - Click a piece to summon"
            screen.blit(self.small_font.render(title, True, COLOR_ACCENT), (self.origin_x, label_y))

            for i, card in enumerate(cards):
                rect = pygame.Rect(self.origin_x + i * 82, y, 72, 84)
                affordable = game_state.can_afford_card(owner, i)
                pygame.draw.rect(screen, COLOR_PANEL if affordable else (36, 30, 26), rect, border_radius=5)
                border_color = PLAYER_COLORS[owner] if affordable else COLOR_MUTED_TEXT
                if game_state.pending_summon and game_state.pending_summon[1].id == card.id and owner == game_state.current_player:
                    border_color = COLOR_SUMMON_OUTLINE
                pygame.draw.rect(screen, border_color, rect, width=2, border_radius=5)

                icon = pygame.Rect(rect.x + 18, rect.y + 20, 36, 34)
                pygame.draw.ellipse(screen, PLAYER_COLORS[owner], icon)
                pygame.draw.ellipse(screen, COLOR_TEXT, icon, width=1)

                name = self.tiny_font.render(card.name[:10], True, COLOR_TEXT)
                cost = self.small_font.render(str(card.value), True, COLOR_ACCENT)
                screen.blit(name, name.get_rect(center=(rect.centerx, rect.y + 10)))
                screen.blit(cost, cost.get_rect(center=(rect.centerx, rect.y + 68)))


def _draw_selected_piece_panel(self, screen, game_state) -> None:
    panel = pygame.Rect(1260, 596, 284, 300)
    pygame.draw.rect(screen, COLOR_PANEL_DARK, panel, border_radius=10)
    pygame.draw.rect(screen, COLOR_BOARD_GRID, panel, width=2, border_radius=10)

    screen.blit(self.section_font.render("SELECTED PIECE", True, COLOR_ACCENT), (1292, 622))

    piece = None
    if self.selected_info_square:
        piece = game_state.board.get_piece(*self.selected_info_square)

    if piece is None:
        self._draw_wrapped(
            screen,
            "Click a battlefield piece to see its movement and Dratp/effect details here.",
            1286,
            676,
            230,
            COLOR_MUTED_TEXT,
        )
        return

    owner_text = f"Player {piece.owner}"
    name_text = f"{piece.name}"
    type_text = f"Type: {piece.piece_type.replace('_', ' ').title()}"
    value_text = f"Value/Cost: {piece.value}G"

    screen.blit(self.small_font.render(name_text[:28], True, COLOR_TEXT), (1286, 668))
    screen.blit(self.small_font.render(owner_text, True, PLAYER_COLORS[piece.owner]), (1286, 692))
    screen.blit(self.small_font.render(type_text, True, COLOR_MUTED_TEXT), (1286, 716))
    screen.blit(self.small_font.render(value_text, True, COLOR_ACCENT), (1286, 740))

    if piece.piece_type == "maseitai":
        ready, reason = game_state.dratp_rules.can_dratp(game_state, piece)
        status = "DRATP: READY" if ready else f"DRATP: {reason}"
        status_color = COLOR_SUCCESS if ready else COLOR_WARNING
        screen.blit(self.small_font.render(status[:32], True, status_color), (1286, 770))

        if getattr(piece, "has_dratped", False):
            badge = pygame.Rect(1286, 798, 82, 24)
            pygame.draw.rect(screen, COLOR_ACCENT, badge, border_radius=4)
            badge_text = self.small_font.render("DRATP'D", True, COLOR_PANEL_DARK)
            screen.blit(badge_text, badge_text.get_rect(center=badge.center))

        effect_text = piece.dratp_description or "No Dratp description loaded yet."
        self._draw_wrapped(screen, effect_text, 1286, 832, 235, COLOR_TEXT)
    elif piece.piece_type == "black_gulled":
        self._draw_wrapped(screen, "Black Gulled move forward and earn 1 Gyullas.", 1286, 782, 235, COLOR_TEXT)
    elif piece.piece_type == "red_gulled":
        self._draw_wrapped(screen, "Red Gulled move forward in one of three directions and earn 3 Gyullas.", 1286, 782, 235, COLOR_TEXT)
    elif piece.piece_type == "navia":
        self._draw_wrapped(screen, "Protect your Navia. If it is captured, you lose.", 1286, 782, 235, COLOR_TEXT)


def _draw_selected_piece_panel(self, screen, game_state) -> None:
    panel = pygame.Rect(1260, 670, 284, 248)
    pygame.draw.rect(screen, COLOR_PANEL_DARK, panel, border_radius=10)
    pygame.draw.rect(screen, COLOR_BOARD_GRID, panel, width=2, border_radius=10)

    screen.blit(self.section_font.render("PIECE EFFECT", True, COLOR_ACCENT), (1304, 692))

    piece = None
    if getattr(self, "selected_info_square", None):
        piece = game_state.board.get_piece(*self.selected_info_square)

    if piece is None:
        self._draw_wrapped(
            screen,
            "Click a battlefield piece to see its effect, Dratp status, and movement notes here.",
            1286,
            742,
            230,
            COLOR_MUTED_TEXT,
        )
        return

    screen.blit(self.small_font.render(piece.name[:28], True, COLOR_TEXT), (1286, 734))
    screen.blit(self.small_font.render(f"Owner: Player {piece.owner}", True, PLAYER_COLORS[piece.owner]), (1286, 756))
    screen.blit(self.small_font.render(f"Type: {piece.piece_type.replace('_', ' ').title()}", True, COLOR_MUTED_TEXT), (1286, 778))
    screen.blit(self.small_font.render(f"Value / Cost: {piece.value}G", True, COLOR_ACCENT), (1286, 800))

    if piece.piece_type == "maseitai":
        ready, reason = game_state.dratp_rules.can_dratp(game_state, piece)
        status = "DRATP: READY" if ready else f"DRATP: {reason}"
        status_color = COLOR_SUCCESS if ready else COLOR_WARNING
        self._draw_wrapped(screen, status, 1286, 826, 235, status_color)

        if getattr(piece, "has_dratped", False):
            badge = pygame.Rect(1444, 798, 78, 24)
            pygame.draw.rect(screen, COLOR_ACCENT, badge, border_radius=4)
            badge_text = self.small_font.render("DRATP'D", True, COLOR_PANEL_DARK)
            screen.blit(badge_text, badge_text.get_rect(center=badge.center))

        effect_text = piece.dratp_description or "No Dratp description loaded yet."
        self._draw_wrapped(screen, effect_text, 1286, 868, 235, COLOR_TEXT)
    elif piece.piece_type == "black_gulled":
        self._draw_wrapped(screen, "Black Gulled move forward and earn 1 Gyullas.", 1286, 832, 235, COLOR_TEXT)
    elif piece.piece_type == "red_gulled":
        self._draw_wrapped(screen, "Red Gulled move forward in one of three directions and earn 3 Gyullas.", 1286, 832, 235, COLOR_TEXT)
    elif piece.piece_type == "navia":
        self._draw_wrapped(screen, "Protect your Navia. If it is captured, you lose.", 1286, 832, 235, COLOR_TEXT)


def _draw_selected_piece_panel(self, screen, game_state) -> None:
    panel = pygame.Rect(1260, 670, 284, 248)
    pygame.draw.rect(screen, COLOR_PANEL_DARK, panel, border_radius=10)
    pygame.draw.rect(screen, COLOR_BOARD_GRID, panel, width=2, border_radius=10)

    screen.blit(self.section_font.render("PIECE EFFECT", True, COLOR_ACCENT), (1304, 692))

    piece = None
    if getattr(self, "selected_info_square", None):
        piece = game_state.board.get_piece(*self.selected_info_square)

    if piece is None:
        self._draw_wrapped(
            screen,
            "Click a battlefield piece to see its effect, Dratp status, and movement notes here.",
            1286,
            742,
            230,
            COLOR_MUTED_TEXT,
        )
        return

    screen.blit(self.small_font.render(piece.name[:28], True, COLOR_TEXT), (1286, 734))
    screen.blit(self.small_font.render(f"Owner: Player {piece.owner}", True, PLAYER_COLORS[piece.owner]), (1286, 756))
    screen.blit(self.small_font.render(f"Type: {piece.piece_type.replace('_', ' ').title()}", True, COLOR_MUTED_TEXT), (1286, 778))
    screen.blit(self.small_font.render(f"Value / Cost: {piece.value}G", True, COLOR_ACCENT), (1286, 800))

    if piece.piece_type == "maseitai":
        ready, reason = game_state.dratp_rules.can_dratp(game_state, piece)
        status = "DRATP: READY" if ready else f"DRATP: {reason}"
        status_color = COLOR_SUCCESS if ready else COLOR_WARNING
        self._draw_wrapped(screen, status, 1286, 826, 235, status_color)

        if getattr(piece, "has_dratped", False):
            badge = pygame.Rect(1444, 798, 78, 24)
            pygame.draw.rect(screen, COLOR_ACCENT, badge, border_radius=4)
            badge_text = self.small_font.render("DRATP'D", True, COLOR_PANEL_DARK)
            screen.blit(badge_text, badge_text.get_rect(center=badge.center))

        effect_text = piece.dratp_description or "No Dratp description loaded yet."
        self._draw_wrapped(screen, effect_text, 1286, 868, 235, COLOR_TEXT)
    elif piece.piece_type == "black_gulled":
        self._draw_wrapped(screen, "Black Gulled move forward and earn 1 Gyullas.", 1286, 832, 235, COLOR_TEXT)
    elif piece.piece_type == "red_gulled":
        self._draw_wrapped(screen, "Red Gulled move forward in one of three directions and earn 3 Gyullas.", 1286, 832, 235, COLOR_TEXT)
    elif piece.piece_type == "navia":
        self._draw_wrapped(screen, "Protect your Navia. If it is captured, you lose.", 1286, 832, 235, COLOR_TEXT)

    def _draw_wrapped(self, screen, text, x, y, max_width, color) -> None:
        words = text.split()
        line = ""
        line_y = y
        for word in words:
            candidate = f"{line} {word}".strip()
            if self.small_font.size(candidate)[0] <= max_width:
                line = candidate
            else:
                if line:
                    screen.blit(self.small_font.render(line, True, color), (x, line_y))
                    line_y += 18
                line = word
        if line:
            screen.blit(self.small_font.render(line, True, color), (x, line_y))


def _board_view_context_menu_at(self, pos):
    if self.context_menu_rect and self.context_menu_rect.collidepoint(pos):
        return "dratp"
    return None

def _board_view_show_context_menu(self, screen, pos, piece):
    self.context_menu_rect = pygame.Rect(pos[0], pos[1], 118, 42)
    pygame.draw.rect(screen, COLOR_PANEL_DARK, self.context_menu_rect, border_radius=6)
    pygame.draw.rect(screen, COLOR_ACCENT, self.context_menu_rect, width=2, border_radius=6)
    label = self.small_font.render("Dratp", True, COLOR_TEXT)
    screen.blit(label, label.get_rect(center=self.context_menu_rect.center))

BoardView.context_menu_at = _board_view_context_menu_at
BoardView.show_context_menu = _board_view_show_context_menu
