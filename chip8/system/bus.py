class Bus:
    def __init__(self):
        self.memory = None
        self.display = None
        self.keyboard = None
        self.sound = None

    def connect_memory(self, memory):
        self.memory = memory

    def connect_display(self, display):
        self.display = display

    def connect_keyboard(self, keyboard):
        self.keyboard = keyboard

    def connect_sound(self, sound):
        self.sound = sound

    # Mémoire
    def read(self, addr):
        return self.memory.read(addr)

    def write(self, addr, value):
        self.memory.write(addr, value)

    # Devices
    def draw(self, x, y, sprite):
        return self.display.draw_sprite(x, y, sprite)

    def is_key_pressed(self, key):
        return self.keyboard.is_pressed(key)
