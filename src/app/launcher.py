import pygame

from src.app.game_app import GameApp
from src.ui.menu_view import MenuView
from src.ui.rules_view import RulesView
from src.utils.constants import FPS, WINDOW_HEIGHT, WINDOW_WIDTH


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
