import pygame
import sys
from chip8.system.emulator import Emulator
from chip8.scenes.main_menu import MainMenu
from chip8.scenes.games_menu import GamesMenu


def main():
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()

    width, height = 900, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("CHIP-8 Emulator Suite")

    clock = pygame.time.Clock()

    # Instances des menus
    main_menu = MainMenu(width, height)
    games_menu = GamesMenu(screen)

    current_state = "MAIN_MENU"

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if current_state == "MAIN_MENU":
            main_menu.update(events)
            main_menu.draw(screen)

            # Gestion des transitions depuis le menu principal
            if main_menu.next_scene == "games":
                current_state = "GAMES_MENU"
                main_menu.next_scene = None  # Reset pour le prochain retour
            elif main_menu.next_scene == "quit":
                pygame.quit()
                sys.exit()
            # Ajoute ici le cas "settings" si besoin

        elif current_state == "GAMES_MENU":
            # Ton GamesMenu actuel possède sa propre boucle 'while True' interne
            # Il renvoie soit le chemin de la ROM, soit "back"
            result = games_menu.run()

            if result == "back":
                current_state = "MAIN_MENU"
            else:
                # Si c'est un chemin de ROM, on lance l'émulateur
                launch_emulator(result)
                # --- LA CORRECTION EST ICI ---
                # Une fois emu.run() terminé, on redéfinit la taille du menu
                screen = pygame.display.set_mode((width, height))
                # On force le rafraîchissement du GamesMenu avec le nouvel écran
                games_menu.screen = screen
                current_state = "GAMES_MENU"

        pygame.display.flip()
        clock.tick(60)


def launch_emulator(rom_path):
    """Initialise et lance l'émulateur avec la ROM choisie"""
    try:
        emu = Emulator()  # Assure-toi que l'Emulator n'appelle pas pygame.init() à nouveau
        emu.load_rom(rom_path)
        emu.run()
    except Exception as e:
        print(f"Erreur lors du lancement de la ROM : {e}")


if __name__ == "__main__":
    main()