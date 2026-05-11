import pygame
import numpy as np


class AudioDevice:
    """Gère le bip sonore du CHIP-8."""
    def __init__(self):
        self.sound = self._generate_beep()  # On prépare le son au démarrage
        self.channel = None
        self.playing = False

    def _generate_beep(self, frequency=440):
        """Crée un bip carré à la fréquence donnée (440 Hz)."""
        sample_rate = 44100 # Qualité audio standard (44100 échantillons/seconde)
        duration = 1.0

        # Vérifie configuration réelle du mixer
        mixer_info = pygame.mixer.get_init()
        if mixer_info is None:
            raise RuntimeError("Mixer not initialized")

        freq, size, channels = mixer_info

        # On génère une onde carrée (sonne comme un bip de jeu rétro)
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = 0.5 * np.sign(np.sin(2 * np.pi * frequency * t))

        audio = (wave * 32767).astype(np.int16) # Conversion au format audio 16 bits

        # On adapte selon que le son est mono ou stéréo
        if channels == 1:
            audio = audio.reshape(-1, 1)
        elif channels == 2:
            audio = np.column_stack((audio, audio))

        return pygame.sndarray.make_sound(audio)

    def start(self):
        """Démarre le bip en boucle."""
        if not self.playing:
            self.channel = self.sound.play(-1)  # -1 = boucle infinie
            self.playing = True

    def stop(self):
        """Arrête le bip."""
        if self.playing and self.channel:
            self.channel.stop()
            self.playing = False
