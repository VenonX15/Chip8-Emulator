import time
import pygame
from chip8.core.cpu import CPU
from chip8.core.memory import Memory
from chip8.core.registers import Registers
from chip8.devices.display import Display
from chip8.devices.keyboard import Keyboard
from chip8.timing.timers import Timers
from chip8.system.config import CPU_HZ, TIMER_HZ
from chip8.debug.debugger import Debugger

class Emulator:
    def __init__(self):
        self.memory = Memory()
        self.registers = Registers()
        self.display = Display()
        self.keyboard = Keyboard()
        self.cpu = CPU(self.memory, self.registers, self.display, self.keyboard)
        self.timers = Timers(self.registers)

        self.cpu_period = 1.0 / CPU_HZ
        self.timer_period = 1.0 / TIMER_HZ

        self.cpu_accumulator = 0.0
        self.timer_accumulator = 0.0

        self.running = True

        self.debugger = Debugger()

    def load_rom(self, path):
        with open(path, "rb") as f:
            self.memory.load_rom(f.read())

    def run(self):
        last_time = time.perf_counter()

        while self.running:
            now = time.perf_counter()
            dt = now - last_time
            last_time = now

            self.cpu_accumulator += dt
            self.timer_accumulator += dt

            # Input
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            self.keyboard.update(events)

            # CPU cycles
            while self.cpu_accumulator >= self.cpu_period:
                self.cpu.cycle()
                self.cpu_accumulator -= self.cpu_period

            # Timers (60Hz)
            while self.timer_accumulator >= self.timer_period:
                self.timers.update()
                self.timer_accumulator -= self.timer_period

            # Render
            self.display.render()

    def reset(self):
        self.memory.reset()
        self.registers.reset()
