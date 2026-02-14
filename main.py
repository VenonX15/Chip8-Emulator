from chip8.system.emulator import Emulator

if __name__ == "__main__":
    emu = Emulator()
    emu.load_rom("roms/Tetris [Fran Dachille, 1991].ch8")
    emu.run()
