import os
import sys
import pygame
import shutil
from tkinter import filedialog, Tk

# Pour éviter d'avoir une petite fenêtre blanche vide au démarrage de tkinter
root = Tk()
root.withdraw()


class GamesMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 28)
        self.small_font = pygame.font.SysFont("consolas", 20)

        # Création du dossier roms s'il n'existe pas
        if not os.path.exists("roms"):
            os.makedirs("roms")

        self.roms = []
        self.refresh_roms()
        self.selected = 0

        # Configuration du bouton "Charger"
        self.btn_rect = pygame.Rect(self.width - 220, self.height - 60, 200, 40)

    def refresh_roms(self):
        """Met à jour la liste des fichiers .ch8 présents dans le dossier roms"""
        self.roms = [f for f in os.listdir("roms") if f.endswith(".ch8")]

    def import_rom(self):
        file_path = filedialog.askopenfilename(
            title="Choisir une ROM Chip-8",
            filetypes=[("Chip-8 ROMs", "*.ch8"), ("All files", "*.*")]
        )

        if file_path:
            filename = os.path.basename(file_path)
            dest_path = os.path.join("roms", filename)

            if not os.path.exists(dest_path):
                shutil.copy(file_path, dest_path)

            self.refresh_roms()
            # --- PETIT AJOUT ICI ---
            if len(self.roms) == 1:
                self.selected = 0

    def run(self):
        while True:
            self.clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if self.roms:  # Seulement si on a des jeux
                        if event.key == pygame.K_UP:
                            self.selected = (self.selected - 1) % len(self.roms)
                        if event.key == pygame.K_DOWN:
                            self.selected = (self.selected + 1) % len(self.roms)
                        if event.key == pygame.K_RETURN:
                            return os.path.join("roms", self.roms[self.selected])

                    if event.key == pygame.K_ESCAPE:
                        return "back"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_rect.collidepoint(mouse_pos):
                        self.import_rom()

            # --- DESSIN ---
            self.screen.fill((5, 5, 5))  # Fond sombre

            # Titre
            title = self.font.render("SELECT A GAME", True, (0, 255, 200))
            self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))

            # Liste des ROMS
            if not self.roms:
                empty_msg = self.font.render("No ROMs found. Import one! ->", True, (150, 50, 50))
                self.screen.blit(empty_msg, (self.width // 2 - empty_msg.get_width() // 2, 200))
            else:
                for i, rom in enumerate(self.roms):
                    is_sel = (i == self.selected)
                    color = (0, 255, 150) if is_sel else (150, 150, 150)
                    prefix = "> " if is_sel else "  "
                    text = self.font.render(f"{prefix}{rom}", True, color)
                    self.screen.blit(text, (100, 150 + i * 40))

            # Dessin du bouton Charger
            btn_color = (0, 200, 150) if self.btn_rect.collidepoint(mouse_pos) else (0, 100, 80)
            pygame.draw.rect(self.screen, btn_color, self.btn_rect, border_radius=5)

            btn_text = self.small_font.render("IMPORT ROM (.ch8)", True, (255, 255, 255))
            self.screen.blit(btn_text, (self.btn_rect.centerx - btn_text.get_width() // 2,
                                        self.btn_rect.centery - btn_text.get_height() // 2))

            # Aide en bas
            help_text = self.small_font.render("ESC: Back | ENTER: Play", True, (100, 100, 100))
            self.screen.blit(help_text, (20, self.height - 40))

            pygame.display.flip()