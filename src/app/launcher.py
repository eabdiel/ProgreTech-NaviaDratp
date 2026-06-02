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

from src.app.game_app import GameApp
from src.ui.menu_view import MenuView
from src.ui.rules_view import RulesView
from src.utils.constants import FPS, WINDOW_HEIGHT, WINDOW_WIDTH


# Launcher owns the main Pygame window and routes the user between menu, rules, setup, and gameplay screens.
class Launcher:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Navia Dratp Digital")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.menu_view = MenuView()
        self.rules_view = RulesView()
        self.game_app = GameApp(self.screen)
        self.current_screen = "menu"

    def run(self) -> None:
        while self.running:
            self._handle_events()
            self._draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

    # Central event router: this keeps screen-specific input isolated from the rest of the application.
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.current_screen == "menu":
                action = self.menu_view.handle_event(event)
                if action == "start_game":
                    self.game_app.reset_to_setup()
                    self.current_screen = "game"
                elif action == "rules":
                    self.current_screen = "rules"
                elif action == "quit":
                    self.running = False

            elif self.current_screen == "rules":
                if self.rules_view.handle_event(event) == "back_to_menu":
                    self.current_screen = "menu"

            elif self.current_screen == "game":
                if self.game_app.handle_event(event) == "back_to_menu":
                    self.current_screen = "menu"

    def _draw(self) -> None:
        if self.current_screen == "menu":
            self.menu_view.draw(self.screen)
        elif self.current_screen == "rules":
            self.rules_view.draw(self.screen)
        elif self.current_screen == "game":
            self.game_app.draw()
