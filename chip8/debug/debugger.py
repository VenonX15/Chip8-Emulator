class Debugger:
    def __init__(self):
        self.paused = False # False = jeu en marche, True = jeu en pause
        self.step_mode = False  # False = normal, True = on avance pas à pas

    def toggle_pause(self):
        """Appuyer sur ce bouton = pause/reprendre le jeu"""
        self.paused = not self.paused

    def step(self):
        """Avance d'une seule instruction (mode pas à pas)"""
        self.step_mode = True
