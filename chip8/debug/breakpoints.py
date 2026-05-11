class Breakpoints:
    def __init__(self):
        self.points = set()  # Liste vide des adresses à surveiller


    def add(self, addr):
        """Ajoute une adresse à surveiller """
        self.points.add(addr)

    def check(self, pc):
        """Vérifie si on doit s'arrêter à l'adresse actuelle"""
        return pc in self.points # True = on s'arrête, False = on continue
