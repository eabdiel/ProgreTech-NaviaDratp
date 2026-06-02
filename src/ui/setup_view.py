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

import pygame

from src.utils.constants import (
    COLOR_ACCENT, COLOR_BACKGROUND, COLOR_BOARD_GRID, COLOR_MUTED_TEXT,
    COLOR_PANEL, COLOR_PANEL_DARK, COLOR_PANEL_HOVER, COLOR_TEXT,
    DRAFT_TARGET_COUNT, PLAYER_COLORS
)


# SetupView renders the draft screen and translates card clicks into roster indexes for SetupState.
class SetupView:
    def __init__(self) -> None:
        self.title_font = pygame.font.SysFont("georgia", 42, bold=True)
        self.section_font = pygame.font.SysFont("georgia", 22, bold=True)
        self.card_font = pygame.font.SysFont("arial", 12, bold=True)
        self.small_font = pygame.font.SysFont("arial", 11)
        self.card_rects: list[tuple[int, pygame.Rect]] = []

    def card_at(self, pos, setup_state):
        self._build_card_rects(setup_state)
        for index, rect in self.card_rects:
            if rect.collidepoint(pos):
                return index
        return None

    def draw(self, screen, setup_state) -> None:
        screen.fill(COLOR_BACKGROUND)
        self._draw_header(screen, setup_state)
        self._draw_draft_panels(screen, setup_state)
        self._draw_roster(screen, setup_state)

    def _draw_header(self, screen, setup_state) -> None:
        panel = pygame.Rect(40, 24, 1480, 100)
        pygame.draw.rect(screen, COLOR_PANEL_DARK, panel, border_radius=16)
        pygame.draw.rect(screen, COLOR_BOARD_GRID, panel, width=2, border_radius=16)

        title = self.title_font.render("Setup Phase - Draft Maseitai", True, COLOR_ACCENT)
        screen.blit(title, (72, 48))

        msg = self.small_font.render(setup_state.status_message, True, COLOR_TEXT)
        screen.blit(msg, (76, 100))

        hint = self.small_font.render(
            f"Both players may choose the same type. Each player drafts {DRAFT_TARGET_COUNT}. R resets. ESC returns to menu.",
            True,
            COLOR_MUTED_TEXT,
        )
        screen.blit(hint, (790, 100))

    def _draw_draft_panels(self, screen, setup_state) -> None:
        for owner, x in [(1, 40), (2, 1190)]:
            rect = pygame.Rect(x, 145, 330, 760)
            pygame.draw.rect(screen, COLOR_PANEL_DARK, rect, border_radius=14)
            pygame.draw.rect(screen, PLAYER_COLORS[owner], rect, width=2, border_radius=14)

            title = self.section_font.render(f"Player {owner} Keep", True, PLAYER_COLORS[owner])
            screen.blit(title, (x + 24, 166))

            count = self.small_font.render(f"{len(setup_state.drafts[owner])}/{DRAFT_TARGET_COUNT} selected", True, COLOR_MUTED_TEXT)
            screen.blit(count, (x + 24, 202))

            y = 238
            for card in setup_state.drafts[owner]:
                card_rect = pygame.Rect(x + 20, y, 290, 54)
                pygame.draw.rect(screen, COLOR_PANEL, card_rect, border_radius=8)
                pygame.draw.rect(screen, PLAYER_COLORS[owner], card_rect, width=1, border_radius=8)
                screen.blit(self.card_font.render(f"#{card.number} {card.name}", True, COLOR_TEXT), (card_rect.x + 10, card_rect.y + 8))
                screen.blit(self.small_font.render(f"{card.value}G", True, COLOR_ACCENT), (card_rect.x + 248, card_rect.y + 8))
                y += 62

    def _draw_roster(self, screen, setup_state) -> None:
        roster_panel = pygame.Rect(395, 145, 770, 760)
        pygame.draw.rect(screen, COLOR_PANEL_DARK, roster_panel, border_radius=14)
        pygame.draw.rect(screen, COLOR_BOARD_GRID, roster_panel, width=2, border_radius=14)

        title = self.section_font.render("Available Maseitai Roster", True, COLOR_ACCENT)
        screen.blit(title, (420, 166))

        active = self.small_font.render(f"Current pick: Player {setup_state.current_player}", True, PLAYER_COLORS[setup_state.current_player])
        screen.blit(active, (920, 172))

        self._build_card_rects(setup_state)
        available = setup_state.available_cards()
        mouse = pygame.mouse.get_pos()

        for index, rect in self.card_rects:
            card = available[index]
            color = COLOR_PANEL_HOVER if rect.collidepoint(mouse) else COLOR_PANEL
            pygame.draw.rect(screen, color, rect, border_radius=6)
            pygame.draw.rect(screen, COLOR_BOARD_GRID, rect, width=1, border_radius=6)

            name = f"#{card.number} {card.name}"
            screen.blit(self.card_font.render(name[:22], True, COLOR_TEXT), (rect.x + 7, rect.y + 5))
            screen.blit(self.small_font.render(f"{card.value}G", True, COLOR_ACCENT), (rect.x + rect.width - 34, rect.y + 5))
            desc = card.description[:42] + ("..." if len(card.description) > 42 else "")
            screen.blit(self.small_font.render(desc, True, COLOR_MUTED_TEXT), (rect.x + 7, rect.y + 25))
            screen.blit(self.small_font.render(card.movement_profile, True, COLOR_MUTED_TEXT), (rect.x + 7, rect.y + 42))

    def _build_card_rects(self, setup_state) -> None:
        self.card_rects.clear()
        available = setup_state.available_cards()
        start_x = 420
        start_y = 220
        card_w = 232
        card_h = 58
        gap_x = 14
        gap_y = 10

        for index, _card in enumerate(available):
            col = index % 3
            row = index // 3
            rect = pygame.Rect(start_x + col * (card_w + gap_x), start_y + row * (card_h + gap_y), card_w, card_h)
            self.card_rects.append((index, rect))
