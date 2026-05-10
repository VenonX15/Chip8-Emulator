import pygame
from chip8.devices.keyboard import REVERSE_KEYMAP


def load_rom_into_memory(memory, rom_path, start=0x200):
    with open(rom_path, "rb") as f:
        rom_data = f.read()

    for i, byte in enumerate(rom_data):
        memory.ram[start + i] = byte

    return len(rom_data)


def analyze_rom_for_keys(memory, rom_size, start=0x200):
    used_registers = set()

    pc = start
    end = start + rom_size

    while pc < end - 1:
        opcode = (memory.ram[pc] << 8) | memory.ram[pc + 1]

        # EX9E - SKP Vx
        if (opcode & 0xF0FF) == 0xE09E:
            vx = (opcode & 0x0F00) >> 8
            used_registers.add(vx)

        # EXA1 - SKNP Vx
        elif (opcode & 0xF0FF) == 0xE0A1:
            vx = (opcode & 0x0F00) >> 8
            used_registers.add(vx)

        # FX0A - LD Vx, K
        elif (opcode & 0xF0FF) == 0xF00A:
            vx = (opcode & 0x0F00) >> 8
            used_registers.add(vx)

        pc += 2

    return sorted(used_registers)


def build_controls_list(used_registers):
    controls = []

    for reg in used_registers:
        if reg in REVERSE_KEYMAP:
            key_name = pygame.key.name(REVERSE_KEYMAP[reg]).upper()
            controls.append(f"{key_name}")

    if not controls:
        controls.append("Dynamic / Any Key")

    return controls
