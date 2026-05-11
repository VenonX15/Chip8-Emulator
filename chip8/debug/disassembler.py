class Disassembler:
    @staticmethod
    def decode(opcode):
        """
        Transforme un nombre opcode en texte compréhensible
        Exemple: 0x6A05 → "LD V10, 0x05" (met le nombre 5 dans le registre V10)
        """
        nnn = opcode & 0x0FFF   # Adresse (3 derniers chiffres hexa)
        nn = opcode & 0x00FF    # Valeur (2 derniers chiffres)
        n = opcode & 0x000F    # Petit nombre (1 chiffre) 
        x = (opcode >> 8) & 0xF  # Registre numéro x   
        y = (opcode >> 4) & 0xF # Registre numéro y

# Instructions 
        if opcode == 0x00E0:
            return "CLS"     # Effacer l'écran
        elif opcode == 0x00EE:
            return "RET"    # Retourner là où on était
        elif opcode & 0xF000 == 0x1000:
            return f"JP {hex(nnn)}"  # Sauter à l'adresse nnn
        elif opcode & 0xF000 == 0x6000:
            return f"LD V{x}, {hex(nn)}"    # Mettre la valeur nn dans Vx
        elif opcode & 0xF000 == 0x7000:
            return f"ADD V{x}, {hex(nn)}"    # Ajouter nn à Vx
        elif opcode & 0xF000 == 0xA000:
            return f"LD I, {hex(nnn)}"  # Mettre nnn dans l'index I
        elif opcode & 0xF000 == 0xD000:
            return f"DRW V{x}, V{y}, {n}"   # DESSINER un sprite (important !)
        else:
            return f"UNK {hex(opcode)}"
