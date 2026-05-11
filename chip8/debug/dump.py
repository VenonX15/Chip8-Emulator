def dump_registers(cpu):
     
      # """Affiche tous les registres (les 16 petites cases mémoire V0 à VF)""
    print("==== REGISTERS ====")
    for i in range(16):
        print(f"V{i:X} = {cpu.reg.V[i]:02X}")   # V0=00, V1=FF, etc.
    print(f"I  = {cpu.reg.I:03X}") 
    print(f"PC = {cpu.reg.PC:03X}") # Compteur programme (où on en est)

def dump_memory(cpu, start=0x200, length=0x100):
    # """Affiche une zone de la mémoire (les données stockées)"""
    print("==== MEMORY ====")
    for i in range(start, start+length, 16):
        row = cpu.mem.ram[i:i+16]
        print(f"{i:03X}: " + " ".join(f"{b:02X}" for b in row))
