import pygame
from chip8.system.config import LOW_RES_WIDTH, LOW_RES_HEIGHT, PIXEL_SCALE

SCALE = 12
COLOR_ON = (255, 255, 255)
COLOR_OFF = (0, 0, 0)

class Display:
    def __init__(self):
        pygame.init()
        self.width = LOW_RES_WIDTH
        self.height = LOW_RES_HEIGHT
        self.screen = pygame.display.set_mode(
            (self.width*SCALE, self.height*SCALE)
        )
        pygame.display.set_caption("CHIP-8 Emulator (Industry)")
        self.buffer = [[0]*self.width for _ in range(self.height)]

    def clear(self):
        self.buffer = [[0]*self.width for _ in range(self.height)]

    def draw_sprite(self, x, y, sprite):
        collision = 0
        for row, byte in enumerate(sprite):
            for bit in range(8):
                if byte & (0x80 >> bit):
                    px = (x + bit) % self.width
                    py = (y + row) % self.height
                    if self.buffer[py][px] == 1:
                        collision = 1
                    self.buffer[py][px] ^= 1
        return collision

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                color = COLOR_ON if self.buffer[y][x] else COLOR_OFF
                pygame.draw.rect(
                    self.screen,
                    color,
                    (x*SCALE, y*SCALE, SCALE, SCALE)
                )
        pygame.display.flip()
