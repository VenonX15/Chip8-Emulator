FONTSET = [
    0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
    0x20, 0x60, 0x20, 0x20, 0x70,  # 1
    0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
    0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
    0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
    0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
    0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
    0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
    0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
    0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
    0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
    0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
    0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
    0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
    0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
    0xF0, 0x80, 0xF0, 0x80, 0x80   # F
]


class Chip8:
    def __init__(self):
        # ===== MEMORY =====
        self.memory = [0] * 4096

        # ===== REGISTERS =====
        self.V = [0] * 16
        self.I = 0
        self.pc = 0x200  # programme commence à 0x200

        # ===== STACK =====
        self.stack = []

        # ===== TIMERS =====
        self.delay_timer = 0
        self.sound_timer = 0

        # ===== DISPLAY =====
        self.display = [[0 for _ in range(64)] for _ in range(32)]

        # ===== KEYBOARD =====
        self.keys = [0] * 16

        # Load fonts
        self.load_fonts()

    def load_fonts(self):
        for i, byte in enumerate(FONTSET):
            self.memory[0x050 + i] = byte

    def load_rom(self, filename):
        with open(filename, "rb") as f:
            rom = f.read()

        for i, byte in enumerate(rom):
            self.memory[0x200 + i] = byte

    def cycle(self):
        opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        self.pc += 2
        self.execute_opcode(opcode)

    def execute_opcode(self, opcode):
        # 00E0 : clear screen
        if opcode == 0x00E0:
            self.display = [[0 for _ in range(64)] for _ in range(32)]

        # 00EE : return from subroutine
        elif opcode == 0x00EE:
            self.pc = self.stack.pop()

        # 1NNN : jump
        elif opcode & 0xF000 == 0x1000:
            self.pc = opcode & 0x0FFF

        # 2NNN : call subroutine
        elif opcode & 0xF000 == 0x2000:
            self.stack.append(self.pc)
            self.pc = opcode & 0x0FFF

        # 6XNN : VX = NN
        elif opcode & 0xF000 == 0x6000:
            x = (opcode & 0x0F00) >> 8
            nn = opcode & 0x00FF
            self.V[x] = nn

        # DXYN : draw sprite
        elif opcode & 0xF000 == 0xD000:
            x = self.V[(opcode & 0x0F00) >> 8]
            y = self.V[(opcode & 0x00F0) >> 4]
            height = opcode & 0x000F

            self.V[0xF] = 0

            for row in range(height):
                sprite = self.memory[self.I + row]

                for col in range(8):
                    pixel = (sprite >> (7 - col)) & 1
                    if pixel:
                        px = (x + col) % 64
                        py = (y + row) % 32

                        if self.display[py][px] == 1:
                            self.V[0xF] = 1

                        self.display[py][px] ^= 1

        # EX9E : skip if key pressed
        elif opcode & 0xF0FF == 0xE09E:
            x = (opcode & 0x0F00) >> 8
            if self.keys[self.V[x]]:
                self.pc += 2

        # EXA1 : skip if key not pressed
        elif opcode & 0xF0FF == 0xE0A1:
            x = (opcode & 0x0F00) >> 8
            if not self.keys[self.V[x]]:
                self.pc += 2

        # FX07 : VX = delay_timer
        elif opcode & 0xF0FF == 0xF007:
            x = (opcode & 0x0F00) >> 8
            self.V[x] = self.delay_timer

        # FX15 : delay_timer = VX
        elif opcode & 0xF0FF == 0xF015:
            x = (opcode & 0x0F00) >> 8
            self.delay_timer = self.V[x]

        # FX18 : sound_timer = VX
        elif opcode & 0xF0FF == 0xF018:
            x = (opcode & 0x0F00) >> 8
            self.sound_timer = self.V[x]

        # FX0A : wait key
        elif opcode & 0xF0FF == 0xF00A:
            x = (opcode & 0x0F00) >> 8
            for i in range(16):
                if self.keys[i]:
                    self.V[x] = i
                    return
            self.pc -= 2

        # 8XY4 : add with carry
        elif opcode & 0xF00F == 0x8004:
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            total = self.V[x] + self.V[y]
            self.V[0xF] = 1 if total > 255 else 0
            self.V[x] = total & 0xFF

        # 8XY5 : sub with borrow
        elif opcode & 0xF00F == 0x8005:
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            self.V[0xF] = 1 if self.V[x] > self.V[y] else 0
            self.V[x] = (self.V[x] - self.V[y]) & 0xFF

        # FX29 : I = font address
        elif opcode & 0xF0FF == 0xF029:
            x = (opcode & 0x0F00) >> 8
            self.I = 0x050 + (self.V[x] * 5)

        # FX33 : BCD
        elif opcode & 0xF0FF == 0xF033:
            x = (opcode & 0x0F00) >> 8
            value = self.V[x]
            self.memory[self.I] = value // 100
            self.memory[self.I + 1] = (value // 10) % 10
            self.memory[self.I + 2] = value % 10

        # FX55 : store registers
        elif opcode & 0xF0FF == 0xF055:
            x = (opcode & 0x0F00) >> 8
            for i in range(x + 1):
                self.memory[self.I + i] = self.V[i]

        # FX65 : load registers
        elif opcode & 0xF0FF == 0xF065:
            x = (opcode & 0x0F00) >> 8
            for i in range(x + 1):
                self.V[i] = self.memory[self.I + i]

        # 7XNN : VX = VX + NN
        elif opcode & 0xF000 == 0x7000:
            x = (opcode & 0x0F00) >> 8
            nn = opcode & 0x00FF
            self.V[x] = (self.V[x] + nn) & 0xFF

        # ANNN : I = NNN
        elif opcode & 0xF000 == 0xA000:
            self.I = opcode & 0x0FFF

        # 3XNN : skip next if VX == NN
        elif opcode & 0xF000 == 0x3000:
            x = (opcode & 0x0F00) >> 8
            nn = opcode & 0x00FF
            if self.V[x] == nn:
                self.pc += 2

        # 4XNN : skip next if VX != NN
        elif opcode & 0xF000 == 0x4000:
            x = (opcode & 0x0F00) >> 8
            nn = opcode & 0x00FF
            if self.V[x] != nn:
                self.pc += 2

        # 5XY0 : skip next if VX == VY
        elif opcode & 0xF00F == 0x5000:
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            if self.V[x] == self.V[y]:
                self.pc += 2

        # 8XY0 : VX = VY
        elif opcode & 0xF00F == 0x8000:
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            self.V[x] = self.V[y]

        # 8XY1 : VX = VX OR VY
        elif opcode & 0xF00F == 0x8001:
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            self.V[x] |= self.V[y]

        # 8XY2 : VX = VX AND VY
        elif opcode & 0xF00F == 0x8002:
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            self.V[x] &= self.V[y]

        # 8XY3 : VX = VX XOR VY
        elif opcode & 0xF00F == 0x8003:
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            self.V[x] ^= self.V[y]

        # 9XY0 : skip next if VX != VY
        elif opcode & 0xF00F == 0x9000:
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            if self.V[x] != self.V[y]:
                self.pc += 2

        # BNNN : jump to NNN + V0
        elif opcode & 0xF000 == 0xB000:
            self.pc = (opcode & 0x0FFF) + self.V[0]

        # CXNN : VX = random & NN
        elif opcode & 0xF000 == 0xC000:
            import random
            x = (opcode & 0x0F00) >> 8
            nn = opcode & 0x00FF
            self.V[x] = random.randint(0, 255) & nn

        else:
            print(f"Opcode inconnu: {hex(opcode)}")

    def update_timers(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            self.sound_timer -= 1
            print("BEEP")
