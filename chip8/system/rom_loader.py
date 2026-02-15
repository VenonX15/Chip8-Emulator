import pygame
from chip8.devices.keyboard import REVERSE_KEYMAP


def load_rom_into_memory(memory, rom_path, start=0x200):
    with open(rom_path, "rb") as f:
        rom_data = f.read()

    for i, byte in enumerate(rom_data):
        memory.ram[start + i] = byte


def analyze_rom_for_keys(memory, start=0x200):
    used_registers = set()

    pc = start
    while pc < len(memory.ram) - 1:
        opcode = (memory.ram[pc] << 8) | memory.ram[pc + 1]

        if (opcode & 0xF0FF) in (0xE09E, 0xE0A1):
            vx = (opcode & 0x0F00) >> 8
            used_registers.add(vx)

        if (opcode & 0xF0FF) == 0xF00A:
            vx = (opcode & 0x0F00) >> 8
            used_registers.add(vx)

        pc += 2

    return sorted(list(used_registers))


def build_controls_list(used_registers):
    controls = []

    for reg in used_registers:
        if reg in REVERSE_KEYMAP:
            key_name = pygame.key.name(REVERSE_KEYMAP[reg]).upper()
            controls.append(f"{key_name}")

    if not controls:
        controls.append("Dynamic / Any Key")

    return controls
