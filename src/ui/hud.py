import pygame

from src.utils.constants import BOARD_ORIGIN_X, COLOR_BOARD_GRID, COLOR_MUTED_TEXT, COLOR_PANEL, COLOR_SUCCESS


class HUD:
    def __init__(self) -> None:
        self.font = pygame.font.SysFont("arial", 18)
        self.small = pygame.font.SysFont("arial", 14)

    def draw(self, screen, game_state) -> None:
        panel = pygame.Rect(BOARD_ORIGIN_X - 40, 928, 660, 24)
        pygame.draw.rect(screen, COLOR_PANEL, panel)
        pygame.draw.rect(screen, COLOR_BOARD_GRID, panel, width=1)
        msg = game_state.status_message[:86]
        screen.blit(self.font.render(msg, True, COLOR_SUCCESS), (panel.x + 20, 928))
        version = self.small.render("v1.1-beta", True, COLOR_MUTED_TEXT)
        screen.blit(version, (panel.right - 60, 932))
