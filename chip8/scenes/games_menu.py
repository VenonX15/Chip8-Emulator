import os
import sys
import pygame

WIDTH = 900
HEIGHT = 600


class GamesMenu:

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 28)

        self.roms = [
            f for f in os.listdir("roms")
            if f.endswith(".ch8")
        ]

        self.selected = 0

    def run(self):

        if not self.roms:
            raise FileNotFoundError("No .ch8 ROMs found in /roms")

        while True:
            self.clock.tick(60)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.roms)

                    if event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.roms)

                    if event.key == pygame.K_RETURN:
                        return os.path.join("roms", self.roms[self.selected])

                    if event.key == pygame.K_ESCAPE:
                        return "back"

            # Draw
            self.screen.fill((0, 0, 0))

            title = self.font.render("Select a Game", True, (0, 255, 200))
            self.screen.blit(title, (350, 100))

            for i, rom in enumerate(self.roms):
                color = (0, 255, 150) if i == self.selected else (255, 255, 255)

                text = self.font.render(
                    f"{i+1}. {rom}",
                    True,
                    color
                )

                self.screen.blit(text, (250, 180 + i * 40))

            pygame.display.flip()
