from dataclasses import dataclass, field
from typing import List
from chip8.system.config import STACK_SIZE


@dataclass
class Registers:
    """
    Représente les registres CPU du CHIP-8.
    """

    V: List[int] = field(default_factory=lambda: [0] * 16)
    I: int = 0
    PC: int = 0x200

    stack: List[int] = field(default_factory=list)

    delay_timer: int = 0
    sound_timer: int = 0

    # ======================
    # Stack operations
    # ======================

    def push(self, value: int) -> None:
        if len(self.stack) >= STACK_SIZE:
            raise OverflowError("Stack overflow (CHIP-8 max 16 levels)")
        self.stack.append(value)

    def pop(self) -> int:
        if not self.stack:
            raise IndexError("Stack underflow")
        return self.stack.pop()

    # ======================
    # Reset CPU state
    # ======================

    def reset(self) -> None:
        for i in range(16):
            self.V[i] = 0
        self.I = 0
        self.PC = 0x200
        self.stack.clear()
        self.delay_timer = 0
        self.sound_timer = 0
