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
        self.base_resolution = (self.width * self.scale, self.height * self.scale)

        self.fullscreen = False
        self.screen = pygame.display.set_mode(
            (self.width * self.scale, self.height * self.scale)
        )
        pygame.display.set_caption("CHIP-8 / SCHIP Emulator")

        # buffer[y][x] = 0 ou 1
        self.buffer = [[0 for _ in range(self.width)] for _ in range(self.height)]

        # quirks
        self.clip_quirk = False  # True pour certains ROMs modernes

        self.font = pygame.font.SysFont("consolas", 18)

    def clear(self):
        """Efface l’écran"""
        self.buffer = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen

        if self.fullscreen:
            info = pygame.display.Info()
            self.screen = pygame.display.set_mode(
                (info.current_w, info.current_h),
                pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode(
                (self.width * self.scale, self.height * self.scale)
            )

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

    def show_controls_overlay(self, title: str, controls: list[str]):
        waiting = True

        overlay_width = 500
        overlay_height = 300

        center_x = (self.width * self.scale - overlay_width) // 2
        center_y = (self.height * self.scale - overlay_height) // 2

        big_font = pygame.font.SysFont("consolas", 28)
        small_font = pygame.font.SysFont("consolas", 22)

        while waiting:
            self.screen.fill((0, 0, 0))

            # boîte centrale
            overlay = pygame.Surface((overlay_width, overlay_height))
            overlay.set_alpha(230)
            overlay.fill((15, 15, 15))
            self.screen.blit(overlay, (center_x, center_y))

            # titre
            title_text = big_font.render(title + " - Controls", True, (0, 255, 0))
            self.screen.blit(title_text, (center_x + 40, center_y + 30))

            # contrôles
            for i, line in enumerate(controls):
                text = small_font.render(line, True, (255, 255, 255))
                self.screen.blit(text, (center_x + 60, center_y + 90 + i * 35))

            # bouton
            ok_text = small_font.render("Press ENTER to Start", True, (255, 255, 0))
            self.screen.blit(ok_text, (center_x + 110, center_y + overlay_height - 60))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False

    def draw_live_keypad_overlay(self, key_state):
        font = pygame.font.SysFont("consolas", 18)

        keypad_layout = [
            [0x1, 0x2, 0x3, 0xC],
            [0x4, 0x5, 0x6, 0xD],
            [0x7, 0x8, 0x9, 0xE],
            [0xA, 0x0, 0xB, 0xF],
        ]

        start_x = 20
        start_y = 20
        box_size = 40
        gap = 8

        for row_index, row in enumerate(keypad_layout):
            for col_index, key in enumerate(row):
                x = start_x + col_index * (box_size + gap)
                y = start_y + row_index * (box_size + gap)

                if key_state[key]:
                    color = (0, 255, 0)  # pressed = green
                else:
                    color = (70, 70, 70)  # idle = dark grey

                pygame.draw.rect(self.screen, color, (x, y, box_size, box_size), border_radius=6)

                label = font.render(hex(key)[2:].upper(), True, (0, 0, 0))
                text_rect = label.get_rect(center=(x + box_size // 2, y + box_size // 2))
                self.screen.blit(label, text_rect)

    def render(self, key_state=None):
        self.screen.fill((0, 0, 0))

        for y in range(self.height):
            for x in range(self.width):
                color = COLOR_ON if self.buffer[y][x] else COLOR_OFF
                pygame.draw.rect(
                    self.screen,
                    color,
                    (x * self.scale, y * self.scale, self.scale, self.scale)
                )

        #if key_state:
        #    self.draw_live_keypad_overlay(key_state)

        pygame.display.flip()

    def set_clip_quirk(self, enabled: bool):
        """Active/désactive le clip pour certains ROMs"""
        self.clip_quirk = enabled