import pygame
from chip8.system.config import (
    LOW_RES_WIDTH, LOW_RES_HEIGHT,
    HIGH_RES_WIDTH, HIGH_RES_HEIGHT,
    PIXEL_SCALE, ENABLE_SCHIP
)

COLOR_ON = (255, 255, 255)
COLOR_OFF = (0, 0, 0)


class Display:
    def __init__(self, high_res: bool = False):
        pygame.init()

        self.high_res = high_res
        self.width = HIGH_RES_WIDTH if high_res else LOW_RES_WIDTH
        self.height = HIGH_RES_HEIGHT if high_res else LOW_RES_HEIGHT
        self.scale = PIXEL_SCALE

        self.screen = pygame.display.set_mode(
            (self.width * self.scale, self.height * self.scale)
        )
        pygame.display.set_caption("CHIP-8 / SCHIP Emulator")

        # buffer[y][x] = 0 ou 1
        self.buffer = [[0 for _ in range(self.width)] for _ in range(self.height)]

        # quirks
        self.clip_quirk = False  # True pour certains ROMs modernes

    def clear(self):
        """Efface l’écran"""
        self.buffer = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def draw_sprite(self, x: int, y: int, sprite: list[int]) -> int:
        """
        Dessine un sprite sur l'écran.
        - x, y: coordonnées (0,0 en haut à gauche)
        - sprite: liste d'octets (8 ou 16 bits pour SCHIP)
        Retourne 1 si collision, 0 sinon.
        """
        collision = 0
        sprite_width = 16 if ENABLE_SCHIP and max(sprite) > 0xFF else 8

        for row, byte in enumerate(sprite):
            for bit in range(sprite_width):
                # détection du bit à dessiner
                if sprite_width == 8:
                    pixel_on = byte & (0x80 >> bit)
                else:
                    # SCHIP 16-bit sprite (split sur 2 bytes)
                    pixel_on = byte & (0x8000 >> bit) if bit < 16 else 0

                if pixel_on:
                    px = x + bit
                    py = y + row

                    if self.clip_quirk:
                        if px >= self.width or py >= self.height:
                            continue
                    else:
                        px %= self.width
                        py %= self.height

                    if self.buffer[py][px]:
                        collision = 1

                    self.buffer[py][px] ^= 1

        return collision

    def render(self):
        """Affiche le buffer à l'écran"""
        for y in range(self.height):
            for x in range(self.width):
                color = COLOR_ON if self.buffer[y][x] else COLOR_OFF
                pygame.draw.rect(
                    self.screen,
                    color,
                    (x * self.scale, y * self.scale, self.scale, self.scale)
                )
        pygame.display.flip()

    def set_clip_quirk(self, enabled: bool):
        """Active/désactive le clip pour certains ROMs"""
        self.clip_quirk = enabled