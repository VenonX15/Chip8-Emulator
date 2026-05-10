class Disassembler:
    @staticmethod
    def decode(opcode):
        nnn = opcode & 0x0FFF
        nn = opcode & 0x00FF
        n = opcode & 0x000F
        x = (opcode >> 8) & 0xF
        y = (opcode >> 4) & 0xF

        if opcode == 0x00E0:
            return "CLS"
        elif opcode == 0x00EE:
            return "RET"
        elif opcode & 0xF000 == 0x1000:
            return f"JP {hex(nnn)}"
        elif opcode & 0xF000 == 0x6000:
            return f"LD V{x}, {hex(nn)}"
        elif opcode & 0xF000 == 0x7000:
            return f"ADD V{x}, {hex(nn)}"
        elif opcode & 0xF000 == 0xA000:
            return f"LD I, {hex(nnn)}"
        elif opcode & 0xF000 == 0xD000:
            return f"DRW V{x}, V{y}, {n}"
        else:
            return f"UNK {hex(opcode)}"
