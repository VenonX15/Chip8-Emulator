class Breakpoints:
    def __init__(self):
        self.points = set()

    def add(self, addr):
        self.points.add(addr)

    def check(self, pc):
        return pc in self.points
