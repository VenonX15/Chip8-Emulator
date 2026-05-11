class Timers:
    """Gère les deux minuteurs du CHIP-8."""
    def __init__(self, registers):
        self.reg = registers    # Les registres de l'émulateur

    def update(self):
        if self.reg.delay_timer > 0:
            self.reg.delay_timer -= 1   # Minuteur général

        if self.reg.sound_timer > 0:
            self.reg.sound_timer -= 1   # Minuteur du bip sonore
