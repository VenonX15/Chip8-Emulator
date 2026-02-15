class Timers:
    def __init__(self, registers):
        self.reg = registers

    def update(self):
        if self.reg.delay_timer > 0:
            self.reg.delay_timer -= 1

        if self.reg.sound_timer > 0:
            self.reg.sound_timer -= 1
