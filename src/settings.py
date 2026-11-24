# Configuration & Constants for Pixel Runner (Game 01 — Modern Multi-Stage Edition)

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 60
TITLE = "Pixel Runner — Multi-Stage Edition"

# Physics
GRAVITY = 0.85
JUMP_STRENGTH = -14.2
DOUBLE_JUMP_STRENGTH = -16.2
GROUND_Y = 430
PLAYER_X = 140

# Speed progression
INITIAL_SPEED = 7.0
MAX_SPEED = 16.5
SPEED_INCREMENT = 0.0016

# Stage Palettes & Configurations
STAGES = [
    {
        "id": 1,
        "name": "CYBER DAWN",
        "threshold": 0,
        "next_threshold": 1200,
        "accent": (0, 240, 255),
        "secondary": (0, 255, 180),
        "sky_top": (12, 10, 28),
        "sky_bottom": (28, 18, 54),
        "ground": (22, 18, 36),
        "ground_line": (0, 240, 255),
        "grid": (55, 35, 90),
        "window_colors": [(0, 240, 255), (180, 230, 255), (255, 240, 150)]
    },
    {
        "id": 2,
        "name": "SUNSET METROPOLIS",
        "threshold": 1200,
        "next_threshold": 3000,
        "accent": (255, 190, 40),
        "secondary": (255, 100, 50),
        "sky_top": (28, 12, 34),
        "sky_bottom": (66, 26, 46),
        "ground": (34, 18, 30),
        "ground_line": (255, 180, 20),
        "grid": (85, 35, 60),
        "window_colors": [(255, 210, 80), (255, 140, 60), (255, 235, 160)]
    },
    {
        "id": 3,
        "name": "NEON NIGHTFALL",
        "threshold": 3000,
        "next_threshold": 5500,
        "accent": (255, 45, 160),
        "secondary": (190, 60, 255),
        "sky_top": (18, 8, 34),
        "sky_bottom": (48, 14, 62),
        "ground": (26, 12, 36),
        "ground_line": (255, 50, 160),
        "grid": (90, 25, 85),
        "window_colors": [(255, 80, 180), (190, 80, 255), (255, 220, 250)]
    },
    {
        "id": 4,
        "name": "APEX OVERDRIVE",
        "threshold": 5500,
        "next_threshold": 999999,
        "accent": (0, 255, 140),
        "secondary": (240, 255, 250),
        "sky_top": (8, 18, 24),
        "sky_bottom": (18, 44, 50),
        "ground": (14, 28, 32),
        "ground_line": (0, 255, 160),
        "grid": (20, 80, 75),
        "window_colors": [(0, 255, 160), (220, 255, 240), (0, 210, 255)]
    }
]

# Modern UI / Glassmorphism Palette Defaults
COLOR_BG_DARK = (12, 10, 24)
COLOR_GLASS_BG = (22, 18, 42, 210)
COLOR_GLASS_BORDER = (0, 240, 255, 120)
COLOR_GLASS_HIGHLIGHT = (255, 255, 255, 30)

# Human Character Palette
SKIN_TONE = (242, 195, 160)
SKIN_SHADOW = (212, 162, 128)
HAIR_COLOR = (42, 28, 22)
HAIR_HIGHLIGHT = (70, 48, 38)

CLOTH_SHIRT = (0, 210, 230)       # Athletic jacket
CLOTH_SHIRT_ACCENT = (0, 150, 180) # Inner shadow/zipper
CLOTH_PANTS = (34, 38, 54)        # Dark tech runner trousers
CLOTH_SHOES = (255, 70, 95)       # Neon red/pink running sneakers
CLOTH_SHOES_SOLES = (255, 255, 255)

# Entities Palette
COLOR_OBSTACLE_GROUND = (255, 45, 110)
COLOR_OBSTACLE_AIR = (255, 180, 0)
COLOR_COIN = (255, 215, 0)
COLOR_COIN_SHINE = (255, 255, 200)

# Typography & Accents
COLOR_TEXT_MAIN = (255, 255, 255)
COLOR_TEXT_ACCENT = (0, 240, 255)
COLOR_TEXT_MUTED = (165, 155, 195)
COLOR_TEXT_GOLD = (255, 215, 0)
COLOR_TEXT_DANGER = (255, 75, 110)
