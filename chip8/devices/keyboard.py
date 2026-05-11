import pygame

# Correspondance entre les touches du clavier PC et les touches du CHIP-8
# Le CHIP-8 a 16 touches : de 0 à F (en hexadécimal)
KEYMAP = {
    pygame.K_1: 0x1,
    pygame.K_2: 0x2,
    pygame.K_3: 0x3,
    pygame.K_4: 0xC,
    pygame.K_q: 0x4,
    pygame.K_w: 0x5,
    pygame.K_e: 0x6,
    pygame.K_r: 0xD,
    pygame.K_a: 0x7,
    pygame.K_s: 0x8,
    pygame.K_d: 0x9,
    pygame.K_f: 0xE,
    pygame.K_z: 0xA,
    pygame.K_x: 0x0,
    pygame.K_c: 0xB,
    pygame.K_v: 0xF,
}

# Le même dictionnaire mais à l'envers (touche CHIP-8 → touche PC)
REVERSE_KEYMAP = {v: k for k, v in KEYMAP.items()}

class Keyboard:
    """Gère les entrées clavier du CHIP-8."""
    def __init__(self):
        self.keys = [False]*16  # Les 16 touches : True si appuyée, False sinon
        self.last_key = None

    def update(self, events):
        """Met à jour l'état des touches à partir des événements pygame."""
        for event in events:
            if event.type == pygame.KEYDOWN:    # Touche enfoncée
                if event.key in KEYMAP:
                    self.keys[KEYMAP[event.key]] = True
                    self.last_key = KEYMAP[event.key]
            elif event.type == pygame.KEYUP:    # Touche relâchée
                if event.key in KEYMAP:
                    self.keys[KEYMAP[event.key]] = False

    def is_pressed(self, key):
        return self.keys[key]

    def wait_key(self):
        """Attend qu'une touche soit appuyée et retourne laquelle."""
        self.last_key = None

        while self.last_key is None:    # On boucle jusqu'à ce qu'on appuie
            events = pygame.event.get()
            self.update(events)
            pygame.time.wait(10)    # Petite pause pour ne pas surcharger le CPU

        key = self.last_key
        self.last_key = None
        return key