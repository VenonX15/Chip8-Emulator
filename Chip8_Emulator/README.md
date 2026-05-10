# CHIP-8 Emulator
___

A CHIP-8 interpreter written in Python. This project emulates the original 1970s virtual machine, allowing you to play classic titles like Pong, Breakout, and Space Invaders.

___

## 🚀 Features
___
- Core Instruction Set: Full implementation of all 35 CHIP-8 opcodes.

- Graphics: Rendered using Pygame at the original 64x32 resolution.

- Sound: Integrated buzzer support for the ST (Sound Timer).

- Configurable Speed: Adjust the CPU clock speed (Hz) to match original hardware or modern preferences.

- Input: Hexadecimal keypad mapping (0-F).

## 🛠️ Technical Specifications 
___
The emulator mimics the original CHIP-8 hardware specifications:
- Memory: 4KB (4096 bytes) of RAM.
- Registers: 16 general-purpose 8-bit registers ($V0$ to $VF$).
- Stack: Used to store return addresses during subroutine calls.
- Timers: 60Hz Delay and Sound timers.