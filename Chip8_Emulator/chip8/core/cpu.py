import random
from chip8.core.instruction import Instruction
from chip8.system.config import ENABLE_SCHIP, FONT_SCHIP_START, FONT_CHIP8_START
from chip8.debug.tracer import Tracer
from chip8.debug.breakpoints import Breakpoints
from chip8.system.config import SHIFT_QUIRK
from chip8.system.config import LOAD_STORE_QUIRK


class CPU:
    def __init__(self, memory, registers, display, keyboard, debug: bool = False):
        self.mem = memory
        self.reg = registers
        self.display = display
        self.keyboard = keyboard
        self.used_keys = set()

        self.debug = debug
        self.tracer = Tracer()
        self.breakpoints = Breakpoints()

    # =====================================================
    # Fetch
    # =====================================================

    def fetch(self) -> int:
        pc = self.reg.PC

        if pc + 1 >= len(self.mem.ram):
            raise MemoryError("PC out of memory bounds")

        return (self.mem.ram[pc] << 8) | self.mem.ram[pc + 1]

    # =====================================================
    # Cycle
    # =====================================================

    def cycle(self) -> None:
        opcode = self.fetch()

        if self.debug:
            self.tracer.trace(self, opcode)

        if self.breakpoints.check(self.reg.PC):
            print(f"🛑 Breakpoint at {hex(self.reg.PC)}")
            input("Press Enter to continue...")

        self.reg.PC += 2
        inst = Instruction(opcode)

        self.execute(inst)

    # =====================================================
    # Execute (Dispatcher)
    # =====================================================

    def execute(self, i: Instruction) -> None:
        op = i.opcode & 0xF000

        if i.opcode == 0x00E0:
            self._cls()

        elif i.opcode == 0x00EE:
            self._ret()

        elif op == 0x1000:
            self._jp(i)

        elif op == 0x2000:
            self._call(i)

        elif op == 0x3000:
            self._se_vx_byte(i)

        elif op == 0x4000:
            self._sne_vx_byte(i)

        elif op == 0x5000 and i.n == 0:
            self._se_vx_vy(i)

        elif op == 0x6000:
            self._ld_vx_byte(i)

        elif op == 0x7000:
            self._add_vx_byte(i)

        elif op == 0x8000:
            self._opcode_8xy(i)

        elif op == 0x9000 and i.n == 0:
            self._sne_vx_vy(i)

        elif op == 0xA000:
            self._ld_i(i)

        elif op == 0xB000:
            self._jp_v0(i)

        elif op == 0xC000:
            self._rnd(i)

        elif op == 0xD000:
            self._drw(i)

        elif op == 0xE000:
            self._opcode_ex(i)

        elif op == 0xF000:
            self._opcode_fx(i)

        else:
            raise ValueError(f"Unknown opcode: {hex(i.opcode)}")

    # =====================================================
    # Instruction Implementations
    # =====================================================

    def _cls(self):
        self.display.clear()

    def _ret(self):
        self.reg.PC = self.reg.pop()

    def _jp(self, i):
        self.reg.PC = i.nnn

    def _call(self, i):
        self.reg.push(self.reg.PC)
        self.reg.PC = i.nnn

    def _se_vx_byte(self, i):
        if self.reg.V[i.x] == i.nn:
            self.reg.PC += 2

    def _sne_vx_byte(self, i):
        if self.reg.V[i.x] != i.nn:
            self.reg.PC += 2

    def _se_vx_vy(self, i):
        if self.reg.V[i.x] == self.reg.V[i.y]:
            self.reg.PC += 2

    def _sne_vx_vy(self, i):
        if self.reg.V[i.x] != self.reg.V[i.y]:
            self.reg.PC += 2

    def _ld_vx_byte(self, i):
        self.reg.V[i.x] = i.nn

    def _add_vx_byte(self, i):
        self.reg.V[i.x] = (self.reg.V[i.x] + i.nn) & 0xFF

    def _ld_i(self, i):
        self.reg.I = i.nnn

    def _jp_v0(self, i):
        self.reg.PC = i.nnn + self.reg.V[0]

    def _rnd(self, i):
        self.reg.V[i.x] = random.getrandbits(8) & i.nn

    def _drw(self, i):
        x = self.reg.V[i.x]
        y = self.reg.V[i.y]

        # Déterminer nombre de lignes à dessiner
        n = i.n
        if ENABLE_SCHIP and n == 0:
            n = 16  # SCHIP high-res sprite

        sprite = self.mem.ram[self.reg.I:self.reg.I + n]
        collision = 0

        for row, byte in enumerate(sprite):
            # SCHIP 16-bit sprite -> 2 octets par ligne
            if ENABLE_SCHIP and byte > 0xFF:
                line_bytes = [(byte >> 8) & 0xFF, byte & 0xFF]
            else:
                line_bytes = [byte]

            for bit_offset, b in enumerate(line_bytes):
                for bit in range(8):
                    if b & (0x80 >> bit):
                        px = (x + bit + bit_offset * 8) % self.display.width
                        py = (y + row) % self.display.height
                        if self.display.buffer[py][px] == 1:
                            collision = 1
                        self.display.buffer[py][px] ^= 1

        self.reg.V[0xF] = 1 if collision else 0

    # =====================================================
    # 8XY*
    # =====================================================

    def _opcode_8xy(self, i):
        V = self.reg.V
        x, y = i.x, i.y

        if i.n == 0x0:
            V[x] = V[y]

        elif i.n == 0x1:
            V[x] |= V[y]

        elif i.n == 0x2:
            V[x] &= V[y]

        elif i.n == 0x3:
            V[x] ^= V[y]

        elif i.n == 0x4:
            s = V[x] + V[y]
            V[0xF] = 1 if s > 0xFF else 0
            V[x] = s & 0xFF

        elif i.n == 0x5:
            V[0xF] = 1 if V[x] > V[y] else 0
            V[x] = (V[x] - V[y]) & 0xFF


        elif i.n == 0x6:
            if SHIFT_QUIRK:
                # Mode moderne
                V[0xF] = V[x] & 1
                V[x] >>= 1
            else:
                # Mode original COSMAC VIP
                V[0xF] = V[y] & 1
                V[x] = V[y] >> 1

        elif i.n == 0x7:
            V[0xF] = 1 if V[y] > V[x] else 0
            V[x] = (V[y] - V[x]) & 0xFF


        elif i.n == 0xE:
            if SHIFT_QUIRK:
                # Mode moderne
                V[0xF] = (V[x] >> 7) & 1
                V[x] = (V[x] << 1) & 0xFF
            else:
                # Mode original COSMAC VIP
                V[0xF] = (V[y] >> 7) & 1
                V[x] = (V[y] << 1) & 0xFF

        else:
            raise ValueError(f"Invalid 8XY opcode: {hex(i.opcode)}")

    # =====================================================
    # EX**
    # =====================================================

    def _opcode_ex(self, i):
        key = self.reg.V[i.x] & 0xF
        subcode = i.opcode & 0x00FF

        if key > 0xF:
            return

        # 🔥 Track dynamic key usage
        self.used_keys.add(key)

        if subcode == 0x9E:
            if self.keyboard.is_pressed(key):
                self.reg.PC += 2

        elif subcode == 0xA1:
            if not self.keyboard.is_pressed(key):
                self.reg.PC += 2

        else:
            print(f"Warning: Unknown EX opcode {hex(i.opcode)}")

    # =====================================================
    # FX**
    # =====================================================

    def _opcode_fx(self, i):
        V = self.reg.V

        if i.nn == 0x07:
            V[i.x] = self.reg.delay_timer

        elif i.nn == 0x0A:
            key = self.keyboard.wait_key()
            V[i.x] = key
            self.used_keys.add(key)

        elif i.nn == 0x15:
            self.reg.delay_timer = V[i.x]

        elif i.nn == 0x18:
            self.reg.sound_timer = V[i.x]

        elif i.nn == 0x1E:
            self.reg.I = (self.reg.I + V[i.x]) & 0xFFF


        elif i.nn == 0x29:
            val = V[i.x]
            if ENABLE_SCHIP and self.display.width == 128:  # high-res
                self.reg.I = FONT_SCHIP_START + val * 10  # chaque caractère = 10 bytes
            else:
                self.reg.I = FONT_CHIP8_START + val * 5  # CHIP-8 classique = 5 bytes

        elif i.nn == 0x33:
            if self.reg.I + 2 >= len(self.mem.ram):
                raise MemoryError("BCD write out of bounds")
            val = V[i.x]
            self.mem.ram[self.reg.I] = val // 100
            self.mem.ram[self.reg.I + 1] = (val // 10) % 10
            self.mem.ram[self.reg.I + 2] = val % 10

        elif i.nn == 0x55:
            end = self.reg.I + i.x
            if end >= len(self.mem.ram):
                raise MemoryError("Memory write out of bounds")
            for idx in range(i.x + 1):
                self.mem.ram[self.reg.I + idx] = V[idx]
            # Comportement original = I est incrémenté
            if not LOAD_STORE_QUIRK:
                self.reg.I += i.x + 1

        elif i.nn == 0x65:
            end = self.reg.I + i.x
            if end >= len(self.mem.ram):
                raise MemoryError("Memory write out of bounds")
            for idx in range(i.x + 1):
                V[idx] = self.mem.ram[self.reg.I + idx]
            # Comportement original = I est incrémenté
            if not LOAD_STORE_QUIRK:
                self.reg.I += i.x + 1

        else:
            raise ValueError(f"Invalid FX opcode: {hex(i.opcode)}")

