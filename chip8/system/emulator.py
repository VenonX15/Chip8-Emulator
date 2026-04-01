import time
import pygame
from chip8.core.cpu import CPU
from chip8.core.memory import Memory
from chip8.core.registers import Registers
from chip8.devices.display import Display
from chip8.devices.keyboard import Keyboard, REVERSE_KEYMAP
from chip8.timing.timers import Timers
from chip8.system.config import CPU_HZ, TIMER_HZ
from chip8.debug.debugger import Debugger
from chip8.devices.sound import AudioDevice

class Emulator:
    def __init__(self):
        self.memory = Memory()
        self.registers = Registers()
        self.display = Display()
        self.keyboard = Keyboard()
        self.cpu = CPU(self.memory, self.registers, self.display, self.keyboard)
        self.timers = Timers(self.registers)
        self.audio = AudioDevice()

        self.cpu_period = 1.0 / CPU_HZ
        self.timer_period = 1.0 / TIMER_HZ

        self.cpu_accumulator = 0.0
        self.timer_accumulator = 0.0

        self.running = True

        self.debugger = Debugger()
        self.control_detection_time = 2.0
        self.control_detection_done = False
        self.start_time = None

    def load_rom(self, path):
        with open(path, "rb") as f:
            self.memory.load_rom(f.read())

    def run(self):
        last_time = time.perf_counter()
        self.start_time = time.perf_counter()

        while self.running:
            now = time.perf_counter()
            dt = now - last_time
            last_time = now

            self.cpu_accumulator += dt
            self.timer_accumulator += dt

            # --- GESTION DES INPUTS ---
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    # Ici on quitte l'application complètement
                    pygame.quit()
                    import sys
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # QUITTER l'émulateur (retour au menu)
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                    # Fullscreen
                    if event.key == pygame.K_F11:
                        self.display.toggle_fullscreen()

            self.keyboard.update(events)

            # --- LOGIQUE CPU ---
            while self.cpu_accumulator >= self.cpu_period:
                self.cpu.cycle()
                self.cpu_accumulator -= self.cpu_period

            # Détection dynamique des contrôles (ton code actuel)
            if not self.control_detection_done:
                if time.perf_counter() - self.start_time > self.control_detection_time:
                    used = sorted(self.cpu.used_keys)
                    controls = self.build_dynamic_controls_list(used)
                    self.display.show_controls_overlay("Detected Controls", controls)
                    self.control_detection_done = True

            # --- TIMERS (60Hz) ---
            while self.timer_accumulator >= self.timer_period:
                self.timers.update()
                self.timer_accumulator -= self.timer_period

            # --- SON ---
            if self.registers.sound_timer > 0:
                self.audio.start()
            else:
                self.audio.stop()

            # --- RENDU ---
            self.display.render(self.keyboard.keys)

        # --- SORTIE DE BOUCLE (Nettoyage) ---
        self.audio.stop()  # On coupe le son en quittant vers le menu

    def build_dynamic_controls_list(self, used_keys):
        controls = []

        for key in used_keys:
            if key in REVERSE_KEYMAP:
                name = pygame.key.name(REVERSE_KEYMAP[key]).upper()
                controls.append(f"{hex(key)[2:].upper()}  →  {name}")

        if not controls:
            controls.append("No controls detected")

        return controls

    def reset(self):
        self.memory.reset()
        self.registers.reset()
