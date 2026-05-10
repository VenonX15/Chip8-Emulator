from dataclasses import dataclass


@dataclass(frozen=True)
class Instruction:
    opcode: int

    @staticmethod
    def from_bytes(high: int, low: int) -> "Instruction":
        return Instruction((high << 8) | low)

    @property
    def nnn(self) -> int:
        return self.opcode & 0x0FFF

    @property
    def nn(self) -> int:
        return self.opcode & 0x00FF

    @property
    def n(self) -> int:
        return self.opcode & 0x000F

    @property
    def x(self) -> int:
        return (self.opcode >> 8) & 0xF

    @property
    def y(self) -> int:
        return (self.opcode >> 4) & 0xF

    @property
    def family(self) -> int:
        return (self.opcode >> 12) & 0xF

    def __repr__(self) -> str:
        return f"<Instruction opcode=0x{self.opcode:04X}>"
