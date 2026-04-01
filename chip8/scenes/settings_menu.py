import sys
import pygame

WIDTH = 900
HEIGHT = 600


class SettingsMenu:

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 32)

        self.options = ["Coming Soon", "Back"]
        self.selected = 0

    def run(self):

        while True:
            self.clock.tick(60)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)

                    if event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)

                    if event.key == pygame.K_RETURN:

                        if self.selected == 1:
                            return "back"

                    if event.key == pygame.K_ESCAPE:
                        return "back"

            # Draw
            self.screen.fill((15, 15, 30))

            title = self.font.render("Settings", True, (0, 255, 200))
            self.screen.blit(title, (380, 150))

            for i, option in enumerate(self.options):
                color = (0, 255, 150) if i == self.selected else (255, 255, 255)

                text = self.font.render(option, True, color)
                self.screen.blit(text, (380, 250 + i * 50))

            pygame.display.flip()
