import pygame 
from chip8 import Chip8, Display
import os


def menu():
    pygame.init()
    screen = pygame.display.set_mode((640, 320))
    pygame.display.set_caption("CHIP-8")

    font = pygame.font.Font(None, 40)
    
    base_path = os.path.dirname(__file__)

    roms = {
    pygame.K_1: os.path.join(base_path, "roms", "Pong_1_player.ch8"),
    pygame.K_2: os.path.join(base_path, "roms", "Pong_2_Pong_hack_David_Winter_1997.ch8")
    }

    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill((0, 0, 0))

        title = font.render("CHIP-8 EMULATOR", True, (255, 255, 255))
        screen.blit(title, (160, 50))

        line1 = font.render("1 - PONG 1 joueur", True, (255, 255, 255))
        screen.blit(line1, (200, 150))

        line2 = font.render("2 - PONG 2 joueur", True, (255, 255, 255))
        screen.blit(line2, (200, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key in roms:
                    return roms[event.key]

        pygame.display.flip()
        clock.tick(60)


def main():
    chip8 = Chip8()

    file_path = menu()
    chip8.load_rom(file_path)

    display = Display(scale=10)
    clock = pygame.time.Clock()
    timer_clock = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        display.handle_input(chip8)

        for _ in range(8):
            chip8.cycle()

        display.draw(chip8.display)

        dt = clock.tick(60)
        timer_clock += dt

        if timer_clock >= 1000 / 60:
            chip8.update_timers()
            timer_clock = 0

    pygame.quit()


if __name__ == "__main__":
    main()