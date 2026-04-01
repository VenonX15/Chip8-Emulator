class Debugger:
    def __init__(self):
        self.paused = False
        self.step_mode = False

    def toggle_pause(self):
        self.paused = not self.paused

    def step(self):
        self.step_mode = True
