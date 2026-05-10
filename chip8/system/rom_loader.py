import pygame
from chip8.devices.keyboard import REVERSE_KEYMAP  # Mapping touche CHIP-8 → touche clavier PC


def load_rom_into_memory(memory, rom_path: str, start: int = 0x200) -> int:
    """
    Charge une ROM depuis le disque en mémoire RAM à partir de l'adresse start (0x200 par défaut).
    Retourne la taille de la ROM en octets.
    """
    with open(rom_path, "rb") as f:
        rom_data = f.read()

    # Copie chaque octet de la ROM dans la RAM à partir de l'adresse de départ
    for i, byte in enumerate(rom_data):
        memory.ram[start + i] = byte

    return len(rom_data)


def analyze_rom_for_keys(memory, rom_size: int, start: int = 0x200) -> list:
    """
    Analyse les opcodes de la ROM pour détecter quels registres Vx
    sont utilisés dans des instructions clavier (EX9E, EXA1, FX0A).
    Retourne la liste triée des registres impliqués dans la gestion des touches.
    """
    used_registers = set()

    pc  = start
    end = start + rom_size

    while pc < end - 1:
        # Lit l'opcode 16 bits à l'adresse courante
        opcode = (memory.ram[pc] << 8) | memory.ram[pc + 1]

        if (opcode & 0xF0FF) == 0xE09E:
            # EX9E — SKP Vx : saute si la touche Vx est pressée
            vx = (opcode & 0x0F00) >> 8
            used_registers.add(vx)

        elif (opcode & 0xF0FF) == 0xE0A1:
            # EXA1 — SKNP Vx : saute si la touche Vx n'est PAS pressée
            vx = (opcode & 0x0F00) >> 8
            used_registers.add(vx)

        elif (opcode & 0xF0FF) == 0xF00A:
            # FX0A — LD Vx, K : attend une pression de touche et la stocke dans Vx
            vx = (opcode & 0x0F00) >> 8
            used_registers.add(vx)

        pc += 2  # Chaque instruction CHIP-8 fait 2 octets

    return sorted(used_registers)


def build_controls_list(used_registers: list) -> list:
    """
    Convertit une liste de registres Vx en noms de touches clavier lisibles.
    Utilise REVERSE_KEYMAP pour traduire l'index CHIP-8 en touche PC.
    Retourne ["Dynamic / Any Key"] si aucune touche spécifique n'est détectée.
    """
    controls = []

    for reg in used_registers:
        if reg in REVERSE_KEYMAP:
            # Récupère le nom de la touche clavier correspondante (ex: "W", "A", "SPACE")
            key_name = pygame.key.name(REVERSE_KEYMAP[reg]).upper()
            controls.append(f"{key_name}")

    # Aucune touche détectée → le jeu gère les touches dynamiquement
    if not controls:
        controls.append("Dynamic / Any Key")

    return controls