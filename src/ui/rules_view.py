import pygame

from src.utils.constants import (
    COLOR_ACCENT, COLOR_BACKGROUND, COLOR_BOARD_GRID, COLOR_PANEL,
    COLOR_MUTED_TEXT, COLOR_TEXT, COLOR_WARNING
)


class RulesView:
    def __init__(self) -> None:
        self.title_font = pygame.font.SysFont("georgia", 42, bold=True)
        self.section_font = pygame.font.SysFont("arial", 23, bold=True)
        self.text_font = pygame.font.SysFont("arial", 18)
        self.small_font = pygame.font.SysFont("arial", 15)
        self.sections = [
            ("Setup Phase", [
                "Players alternate choosing Maseitai before the match.",
                "Each player drafts 7 Maseitai into their Keep.",
                "After both Keeps are filled, the match starts.",
            ]),
            ("Basic pieces", [
                "Navia moves like a chess king.",
                "Black Gulled move forward and earn 1 Gyullas.",
                "Red Gulled move forward in one of three directions and earn 3 Gyullas.",
                "These Gulled are always placed automatically at game start.",
            ]),
            ("Board zones", [
                "Summon spaces are the three left and three right spaces beside each Navia.",
                "Also summon spaces: 1,0; 1,6; 5,0; and 5,6.",
                "At game start only 4 summon spaces are open because Gulled occupy the others.",
                "Gyullas Reduction Zone is row 3, columns 1 through 5.",
            ]),
            ("Game actions", [
                "Move one battlefield piece.",
                "OR summon one Maseitai from your pool if you can afford it.",
                "Capture enemy pieces for Gyullas.",
                "Capture the opposing Navia to win.",
            ]),
        ]

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back_to_menu"
        if event.type == pygame.MOUSEBUTTONDOWN:
            return "back_to_menu"
        return None

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(COLOR_BACKGROUND)
        panel = pygame.Rect(100, 70, 1360, 800)
        pygame.draw.rect(screen, COLOR_PANEL, panel, border_radius=18)
        pygame.draw.rect(screen, COLOR_BOARD_GRID, panel, width=3, border_radius=18)

        screen.blit(self.title_font.render("Rules Reference", True, COLOR_TEXT), (140, 110))
        screen.blit(self.small_font.render("Click anywhere or press ESC to return.", True, COLOR_MUTED_TEXT), (142, 160))

        positions = [(140, 225), (830, 225), (140, 510), (830, 510)]
        for (title, bullets), (x, y) in zip(self.sections, positions):
            screen.blit(self.section_font.render(title, True, COLOR_ACCENT), (x, y))
            line_y = y + 42
            for bullet in bullets:
                screen.blit(self.text_font.render(f"- {bullet}", True, COLOR_TEXT), (x, line_y))
                line_y += 32

        source = self.small_font.render("Full public reference remains available on the project website.", True, COLOR_WARNING)
        screen.blit(source, (140, 820))
