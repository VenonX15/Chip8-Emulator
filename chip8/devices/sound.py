import pygame
import numpy as np


class AudioDevice:
    def __init__(self):
        self.sound = self._generate_beep()
        self.channel = None
        self.playing = False

    def _generate_beep(self, frequency=440):
        sample_rate = 44100
        duration = 1.0

        # Vérifie configuration réelle du mixer
        mixer_info = pygame.mixer.get_init()
        if mixer_info is None:
            raise RuntimeError("Mixer not initialized")

        freq, size, channels = mixer_info

        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = 0.5 * np.sign(np.sin(2 * np.pi * frequency * t))

        audio = (wave * 32767).astype(np.int16)

        # 🔥 Adapter automatiquement au nombre de channels
        if channels == 1:
            audio = audio.reshape(-1, 1)
        elif channels == 2:
            audio = np.column_stack((audio, audio))

        return pygame.sndarray.make_sound(audio)

    def start(self):
        if not self.playing:
            self.channel = self.sound.play(-1)
            self.playing = True

    def stop(self):
        if self.playing and self.channel:
            self.channel.stop()
            self.playing = False
