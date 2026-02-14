# =========================
# Mémoire
# =========================
MEMORY_SIZE = 4096

PROGRAM_START = 0x200

FONT_CHIP8_START = 0x050
FONT_SCHIP_START = 0x100
FONTSET_START = FONT_CHIP8_START

# =========================
# CPU / Timing
# =========================
CPU_HZ = 700          # fréquence CPU (500–1000 recommandé)
TIMER_HZ = 60         # fréquence des timers CHIP-8


# =========================
# Display
# =========================
LOW_RES_WIDTH = 64
LOW_RES_HEIGHT = 32

HIGH_RES_WIDTH = 128
HIGH_RES_HEIGHT = 64

PIXEL_SCALE = 10      # facteur d’agrandissement fenêtre
VSYNC = False         # pygame (optionnel)


# =========================
# Stack
# =========================
STACK_SIZE = 16       # historique, mais utile pour vérification


# =========================
# SCHIP / Extensions
# =========================
ENABLE_SCHIP = True
ENABLE_XOCHIP = False


# =========================
# Debug
# =========================
DEBUG = False         # trace CPU
DEBUG_STEP = False   # step-by-step au démarrage
LOG_LEVEL = "INFO"   # INFO / DEBUG / WARNING


# =========================
# ROM
# =========================
DEFAULT_ROM_PATH = "roms/PONG.ch8"


# =========================
# Keyboard mapping (logique)
# =========================
CHIP8_KEYS = [
    0x1, 0x2, 0x3, 0xC,
    0x4, 0x5, 0x6, 0xD,
    0x7, 0x8, 0x9, 0xE,
    0xA, 0x0, 0xB, 0xF
]

# =========================
# Compatibility / Quirks
# =========================

# SHIFT instructions (8XY6 / 8XYE)
# False = comportement original COSMAC VIP (VX = VY >> 1)
# True  = comportement moderne (VX >>= 1)
SHIFT_QUIRK = False

# FX55 / FX65 modifies I register
# False = comportement original (I est incrémenté)
# True  = I reste inchangé (moderne)
LOAD_STORE_QUIRK = False

# Drawing behavior when sprite exceeds screen bounds
# False = wrap around (original VIP)
# True  = clip at screen edges
CLIP_QUIRK = False

# VF reset behavior for logic ops (8XY1, 8XY2, 8XY3)
# False = ne pas modifier VF (original)
# True  = VF = 0 (certaines implémentations modernes)
LOGIC_VF_RESET = False
