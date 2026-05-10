import pygame

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

REVERSE_KEYMAP = {v: k for k, v in KEYMAP.items()}

class Keyboard:
    def __init__(self):
        self.keys = [False]*16
        self.last_key = None

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in KEYMAP:
                    self.keys[KEYMAP[event.key]] = True
                    self.last_key = KEYMAP[event.key]
            elif event.type == pygame.KEYUP:
                if event.key in KEYMAP:
                    self.keys[KEYMAP[event.key]] = False

    def is_pressed(self, key):
        return self.keys[key]

    def wait_key(self):
        self.last_key = None

        while self.last_key is None:
            events = pygame.event.get()
            self.update(events)
            pygame.time.wait(10)

        key = self.last_key
        self.last_key = None
        return key