import time

class Clock:
    """Fait tourner l'émulateur à la bonne vitesse."""
    def __init__(self, hz):
        self.hz = hz
        self.period = 1.0 / hz  # Durée d'un tick en secondes
        self.last_time = time.perf_counter()

    def tick(self):
        """Attend si on va trop vite."""
        now = time.perf_counter()   # Heure actuelle
        elapsed = now - self.last_time  # Temps passé depuis le dernier tick
        if elapsed < self.period:
            time.sleep(self.period - elapsed)   # On attend le temps restant
        self.last_time = time.perf_counter()    # On remet le chrono à zéro
