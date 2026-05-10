import random
import pygame
import math


class MainMenu:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.next_scene = None

        # --- Background Dynamique (Parallaxe) ---
        # On stocke (x, y, vitesse, taille)
        self.stars = [
            [random.randint(0, self.width), random.randint(0, self.height), random.random() * 2 + 0.5,
             random.randint(1, 3)]
            for _ in range(100)
        ]

        # --- Polices ---
        # Utilisation d'une police système monospaced pour le look rétro
        self.title_font = pygame.font.SysFont("consolas", 80, bold=True)
        self.menu_font = pygame.font.SysFont("consolas", 36)

        self.options = ["Games", "Settings", "Quit"]
        self.selected = 0

        # Mapping des touches pour éviter les IF en cascade
        self.key_map = {
            pygame.K_1: 0, pygame.K_KP1: 0,
            pygame.K_2: 1, pygame.K_KP2: 1,
            pygame.K_3: 2, pygame.K_KP3: 2
        }

        # Animation de pulsation
        self.animation_counter = 0

    def update(self, events):
        self.animation_counter += 0.05

        # Update des étoiles (mouvement vers le bas)
        for star in self.stars:
            star[1] += star[2]  # On ajoute la vitesse à Y
            if star[1] > self.height:
                star[1] = 0
                star[0] = random.randint(0, self.width)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)

                # Sélection directe par numéro
                elif event.key in self.key_map:
                    self.selected = self.key_map[event.key]
                    self._trigger_selection()

                elif event.key == pygame.K_RETURN:
                    self._trigger_selection()

    def _trigger_selection(self):
        actions = ["games", "quit"]
        self.next_scene = actions[self.selected]

    def draw(self, screen):
        screen.fill((5, 5, 15))  # Bleu très foncé pour plus de profondeur

        # 1. Dessin des étoiles
        for star in self.stars:
            alpha = random.randint(150, 255)  # Scintillement
            pygame.draw.circle(screen, (alpha, alpha, alpha), (int(star[0]), int(star[1])), star[3])

        # 2. Titre avec effet de "pulsation"
        # On utilise math.sin pour faire varier la luminosité
        pulse = int(200 + 55 * math.sin(self.animation_counter))
        title_color = (pulse, pulse, 255)  # Le titre pulse en bleu/blanc

        title_surf = self.title_font.render("CHIP-8", True, title_color)
        subtitle_surf = self.menu_font.render("EMULATOR STATION", True, (100, 100, 100))

        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 120))
        screen.blit(subtitle_surf, (self.width // 2 - subtitle_surf.get_width() // 2, 200))

        # 3. Menu Options
        start_y = 350
        for i, option in enumerate(self.options):
            is_selected = (i == self.selected)

            # Couleur et texte
            color = (0, 255, 200) if is_selected else (150, 150, 150)
            prefix = "> " if is_selected else "  "

            # Petit effet de décalage vers la droite pour l'option sélectionnée
            x_offset = 15 if is_selected else 0

            text_surf = self.menu_font.render(f"{prefix}{i + 1}. {option}", True, color)

            # Centrage horizontal avec l'offset
            pos_x = self.width // 2 - text_surf.get_width() // 2 + x_offset
            pos_y = start_y + i * 60

            # Ombre portée pour le texte sélectionné
            if is_selected:
                shadow = self.menu_font.render(f"{prefix}{i + 1}. {option}", True, (0, 50, 50))
                screen.blit(shadow, (pos_x + 2, pos_y + 2))

            screen.blit(text_surf, (pos_x, pos_y))

        # 4. Footer (Aide)
        help_surf = self.menu_font.render("USE ARROWS & ENTER", True, (50, 50, 50))
        screen.blit(help_surf, (self.width // 2 - help_surf.get_width() // 2, self.height - 50))