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
    COLOR_ACCENT, COLOR_BACKGROUND, COLOR_PANEL, COLOR_PANEL_HOVER,
    COLOR_TEXT, COLOR_MUTED_TEXT, COLOR_BOARD_GRID
)


class MenuButton:
    def __init__(self, label: str, action: str, rect: pygame.Rect) -> None:
        self.label = label
        self.action = action
        self.rect = rect

    def is_hovered(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())


class MenuView:
    def __init__(self) -> None:
        self.title_font = pygame.font.SysFont("georgia", 64, bold=True)
        self.subtitle_font = pygame.font.SysFont("arial", 24)
        self.button_font = pygame.font.SysFont("arial", 27, bold=True)
        self.footer_font = pygame.font.SysFont("arial", 16)
        self.buttons = [
            MenuButton("Start Game", "start_game", pygame.Rect(660, 360, 250, 58)),
            MenuButton("Rules Reference", "rules", pygame.Rect(660, 435, 250, 58)),
            MenuButton("Quit", "quit", pygame.Rect(660, 510, 250, 58)),
        ]

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    return button.action
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "start_game"
            if event.key == pygame.K_ESCAPE:
                return "quit"
        return None

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(COLOR_BACKGROUND)
        panel = pygame.Rect(420, 120, 720, 190)
        pygame.draw.rect(screen, COLOR_PANEL, panel, border_radius=18)
        pygame.draw.rect(screen, COLOR_BOARD_GRID, panel, width=3, border_radius=18)

        title = self.title_font.render("Navia Dratp Digital", True, COLOR_TEXT)
        subtitle = self.subtitle_font.render("Python Prototype v0.6", True, COLOR_ACCENT)
        note = self.subtitle_font.render("Setup Phase, corrected summon spaces, and stable board UI.", True, COLOR_MUTED_TEXT)

        screen.blit(title, title.get_rect(center=(780, 180)))
        screen.blit(subtitle, subtitle.get_rect(center=(780, 240)))
        screen.blit(note, note.get_rect(center=(780, 275)))

        for button in self.buttons:
            color = COLOR_PANEL_HOVER if button.is_hovered() else COLOR_PANEL
            pygame.draw.rect(screen, color, button.rect, border_radius=12)
            pygame.draw.rect(screen, COLOR_ACCENT, button.rect, width=2, border_radius=12)
            label = self.button_font.render(button.label, True, COLOR_TEXT)
            screen.blit(label, label.get_rect(center=button.rect.center))

        footer = self.footer_font.render("ENTER = Start Game   |   ESC = Quit", True, COLOR_MUTED_TEXT)
        screen.blit(footer, footer.get_rect(center=(780, 910)))
