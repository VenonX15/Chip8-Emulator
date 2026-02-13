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
