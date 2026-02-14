import os
import pygame
from chip8.system.emulator import Emulator

def rom_menu():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Select ROM")

    font = pygame.font.SysFont("consolas", 24)

    roms = [f for f in os.listdir("roms") if f.endswith(".ch8")]
    selected = 0
    running = True

    while running:
        screen.fill((0, 0, 0))

        title = font.render("Select a ROM (ENTER to launch)", True, (255,255,255))
        screen.blit(title, (100, 50))

        for i, rom in enumerate(roms):
            color = (0,255,0) if i == selected else (255,255,255)
            text = font.render(rom, True, color)
            screen.blit(text, (150, 120 + i*30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(roms)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(roms)
                elif event.key == pygame.K_RETURN:
                    return os.path.join("roms", roms[selected])

if __name__ == "__main__":
    emu = Emulator()
    rom_path = rom_menu()
    emu.load_rom(rom_path)
    emu.run()
