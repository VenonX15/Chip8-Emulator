from chip8.system.emulator import Emulator

if __name__ == "__main__":
    emu = Emulator()
    emu.load_rom("roms/Pong_1_player.ch8")
    emu.run()
