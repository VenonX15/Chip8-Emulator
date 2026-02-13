from chip8.system.emulator import Emulator

if __name__ == "__main__":
    emu = Emulator()
    emu.load_rom("roms/PONG.ch8")
    emu.run()
