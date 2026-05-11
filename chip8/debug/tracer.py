from chip8.debug.disassembler import Disassembler

class Tracer:
    def trace(self, cpu, opcode: int):
        #Affiche en temps réel : l'instruction, le PC, les registres
        asm = Disassembler.decode(opcode)   # Traduit l'opcode en texte
        regs = " ".join(
            f"V{i:X}={cpu.reg.V[i]:02X}" for i in range(16)
        )

        print(
            f"[PC={cpu.reg.PC:04X}] {asm} | "
            f"I={cpu.reg.I:03X} | {regs}"
        )
