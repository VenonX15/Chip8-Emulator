import sys
import pygame

# Dimensions de la fenêtre (partagées avec les autres scènes)
WIDTH  = 900
HEIGHT = 600


class SettingsMenu:
    """
    Écran des paramètres de l'émulateur.
    Actuellement un placeholder ("Coming Soon") avec un bouton de retour.
    """

    def __init__(self, screen):
        self.screen   = screen
        self.clock    = pygame.time.Clock()
        self.font     = pygame.font.SysFont("consolas", 32)

        # Options disponibles (Coming Soon est non-fonctionnel pour l'instant)
        self.options  = ["Coming Soon", "Back"]
        self.selected = 0  # Index de l'option sélectionnée

    def run(self) -> str:
        """
        Boucle principale du menu paramètres.

        Retourne :
            "back" pour revenir au menu principal.
        """
        while True:
            self.clock.tick(60)  # Limite à 60 FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        # Remonte dans la liste avec wrap-around
                        self.selected = (self.selected - 1) % len(self.options)

                    if event.key == pygame.K_DOWN:
                        # Descend dans la liste avec wrap-around
                        self.selected = (self.selected + 1) % len(self.options)

                    if event.key == pygame.K_RETURN:
                        # Seul "Back" (index 1) est fonctionnel pour l'instant
                        if self.selected == 1:
                            return "back"

                    if event.key == pygame.K_ESCAPE:
                        # Raccourci direct pour revenir en arrière
                        return "back"

            # --- Rendu ---
            self.screen.fill((15, 15, 30))  # Fond bleu nuit

            # Titre de la page
            title = self.font.render("Settings", True, (0, 255, 200))
            self.screen.blit(title, (380, 150))

            # Liste des options (cyan si sélectionnée, blanc sinon)
            for i, option in enumerate(self.options):
                color = (0, 255, 150) if i == self.selected else (255, 255, 255)
                text  = self.font.render(option, True, color)
                self.screen.blit(text, (380, 250 + i * 50))

            pygame.display.flip()  # Met à jour l'affichage