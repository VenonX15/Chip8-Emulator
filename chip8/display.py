import pygame

KEY_MAP = {
    pygame.K_x: 0x0,
    pygame.K_1: 0x1,
    pygame.K_2: 0x2,
    pygame.K_3: 0x3,
    pygame.K_q: 0x4,
    pygame.K_w: 0x5,
    pygame.K_e: 0x6,
    pygame.K_a: 0x7,
    pygame.K_s: 0x8,
    pygame.K_d: 0x9,
    pygame.K_z: 0xA,
    pygame.K_c: 0xB,
    pygame.K_4: 0xC,
    pygame.K_r: 0xD,
    pygame.K_f: 0xE,
    pygame.K_v: 0xF,
}


class Display:
    def __init__(self, scale=10):
        pygame.init()
        self.scale = scale
        self.screen = pygame.display.set_mode((64 * scale, 32 * scale))
        pygame.display.set_caption("CHIP-8 Emulator")

    def draw(self, display):
        self.screen.fill((0, 0, 0))

        for y in range(32):
            for x in range(64):
                if display[y][x]:
                    pygame.draw.rect(
                        self.screen,
                        (255, 255, 255),
                        pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale)
                    )

        pygame.display.flip()

    def handle_input(self, chip8):
        keys = pygame.key.get_pressed()
        for key, value in KEY_MAP.items():
            chip8.keys[value] = 1 if keys[key] else 0
