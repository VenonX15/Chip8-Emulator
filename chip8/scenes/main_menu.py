import random
import pygame


class MainMenu:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.next_scene = None

        # -------------------------
        # Background stars (STATIC)
        # -------------------------
        self.stars = [
            (
                random.randint(0, self.width),
                random.randint(0, self.height)
            )
            for _ in range(150)
        ]

        # -------------------------
        # Fonts
        # -------------------------
        self.title_font = pygame.font.SysFont("consolas", 72, bold=True)
        self.menu_font = pygame.font.SysFont("consolas", 34)

        # -------------------------
        # Menu options (numbered)
        # -------------------------
        self.options = [
            "1. Games",
            "2. Settings",
            "3. Quit"
        ]

        self.selected = 0

    # ==========================================================
    # UPDATE
    # ==========================================================
    def update(self, events):

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)

                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)

                elif event.key == pygame.K_RETURN:

                    if self.selected == 0:
                        self.next_scene = "games"

                    elif self.selected == 1:
                        self.next_scene = "settings"

                    elif self.selected == 2:
                        self.next_scene = "quit"

                # Raccourcis numériques directs
                elif event.key == pygame.K_1:
                    self.next_scene = "games"

                elif event.key == pygame.K_2:
                    self.next_scene = "settings"

                elif event.key == pygame.K_3:
                    self.next_scene = "quit"

    # ==========================================================
    # DRAW
    # ==========================================================
    def draw(self, screen):

        # Fond noir pur
        screen.fill((0, 0, 0))

        # Etoiles blanches statiques
        for star in self.stars:
            pygame.draw.circle(screen, (255, 255, 255), star, 2)

        # -------------------------
        # Title (WHITE)
        # -------------------------
        title_surface = self.title_font.render(
            "CHIP-8 EMULATOR",
            True,
            (255, 255, 255)
        )

        screen.blit(
            title_surface,
            (
                self.width // 2 - title_surface.get_width() // 2,
                150
            )
        )

        # -------------------------
        # Menu Options
        # -------------------------
        start_y = 320
        spacing = 60

        for i, option in enumerate(self.options):

            if i == self.selected:
                color = (200, 200, 200)  # légèrement grisé
            else:
                color = (255, 255, 255)

            text_surface = self.menu_font.render(option, True, color)

            screen.blit(
                text_surface,
                (
                    self.width // 2 - text_surface.get_width() // 2,
                    start_y + i * spacing
                )
            )
