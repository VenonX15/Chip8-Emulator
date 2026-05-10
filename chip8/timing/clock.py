import time

class Clock:
    """Fait tourner l'émulateur à la bonne vitesse."""
    def __init__(self, hz):
        self.hz = hz
        self.period = 1.0 / hz
        self.last_time = time.perf_counter()

    def tick(self):
        """Attend si on va trop vite."""
        now = time.perf_counter()
        elapsed = now - self.last_time
        if elapsed < self.period:
            time.sleep(self.period - elapsed)
        self.last_time = time.perf_counter()
