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

from src.utils.constants import COLOR_BOARD_GRID, COLOR_MUTED_TEXT, COLOR_PANEL, COLOR_SUCCESS, WINDOW_WIDTH


class HUD:
    """Bottom status strip.

    The status bar is intentionally anchored to the bottom of the window while the
    bottom Maseitai card row sits above it with enough spacing for card costs.
    """

    def __init__(self) -> None:
        self.font = pygame.font.SysFont("arial", 18)
        self.small = pygame.font.SysFont("arial", 14)

    def draw(self, screen, game_state) -> None:
        panel = pygame.Rect(500, 930, 650, 24)
        pygame.draw.rect(screen, COLOR_PANEL, panel)
        pygame.draw.rect(screen, COLOR_BOARD_GRID, panel, width=1)

        msg = game_state.status_message[:86]
        screen.blit(self.font.render(msg, True, COLOR_SUCCESS), (panel.x + 18, panel.y + 1))

        version = self.small.render("v1.5-beta", True, COLOR_MUTED_TEXT)
        screen.blit(version, (panel.right - 72, panel.y + 5))
