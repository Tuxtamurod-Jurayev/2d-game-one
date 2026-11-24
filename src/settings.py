# Configuration & Constants for Pixel Runner (Multi-Stage Subway Heroes Edition)

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 60
TITLE = "Pixel Runner — Subway Heroes Edition"

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

# ----------------------------------------------------
# 4 SELECTABLE HEROES FROM SUBWAY RUNNERS
# ----------------------------------------------------
CHARACTERS = [
    {
        "id": "jake",
        "name": "JAKE",
        "title": "THE SUBWAY CAPTAIN",
        "desc": "Cap backwards & denim vest. Balanced runner.",
        "skin_tone": (244, 202, 172),
        "skin_shadow": (216, 170, 138),
        "hair_color": (52, 34, 24),
        "accent_color": (0, 240, 255),
        "tag_color": (255, 75, 95)
    },
    {
        "id": "tricky",
        "name": "TRICKY",
        "title": "THE ACROBAT SKATER",
        "desc": "Red beanie & blonde pigtails. Agile jumper.",
        "skin_tone": (250, 215, 190),
        "skin_shadow": (224, 182, 154),
        "hair_color": (250, 218, 94),
        "accent_color": (255, 60, 80),
        "tag_color": (255, 215, 0)
    },
    {
        "id": "fresh",
        "name": "FRESH",
        "title": "THE RHYTHM MASTER",
        "desc": "Tall high-top fade & nerd glasses. High swagger.",
        "skin_tone": (165, 105, 65),
        "skin_shadow": (130, 75, 45),
        "hair_color": (20, 15, 15),
        "accent_color": (50, 225, 80),
        "tag_color": (255, 50, 70)
    },
    {
        "id": "yutani",
        "name": "YUTANI",
        "title": "THE TECH ALIEN",
        "desc": "Green monster onesie & 4 arms. Cosmic genius.",
        "skin_tone": (245, 205, 180),
        "skin_shadow": (215, 172, 145),
        "hair_color": (25, 20, 30),
        "accent_color": (120, 230, 40),
        "tag_color": (190, 60, 255)
    }
]

# ----------------------------------------------------
# 4 PROGRESSIVE STAGES
# ----------------------------------------------------
STAGES = [
    {
        "id": 1,
        "name": "CYBER DAWN",
        "threshold": 0,
        "next_threshold": 1200,
        "accent": (0, 240, 255),
        "secondary": (0, 255, 180),
        "sky_top": (10, 8, 26),
        "sky_bottom": (26, 16, 52),
        "ground": (20, 16, 32),
        "ground_line": (0, 240, 255),
        "grid": (50, 32, 85),
        "moon_color": (220, 245, 255),
        "moon_glow": (0, 240, 255, 35),
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
        "sky_bottom": (70, 28, 50),
        "ground": (34, 18, 30),
        "ground_line": (255, 180, 20),
        "grid": (85, 35, 60),
        "moon_color": (255, 210, 140),
        "moon_glow": (255, 140, 40, 40),
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
        "sky_bottom": (50, 14, 64),
        "ground": (26, 12, 36),
        "ground_line": (255, 50, 160),
        "grid": (90, 25, 85),
        "moon_color": (255, 190, 240),
        "moon_glow": (255, 50, 160, 35),
        "window_colors": [(255, 80, 180), (190, 80, 255), (255, 220, 250)]
    },
    {
        "id": 4,
        "name": "APEX OVERDRIVE",
        "threshold": 5500,
        "next_threshold": 999999,
        "accent": (0, 255, 140),
        "secondary": (240, 255, 250),
        "sky_top": (6, 16, 22),
        "sky_bottom": (16, 42, 48),
        "ground": (12, 24, 28),
        "ground_line": (0, 255, 160),
        "grid": (18, 75, 70),
        "moon_color": (200, 255, 235),
        "moon_glow": (0, 255, 160, 40),
        "window_colors": [(0, 255, 160), (220, 255, 240), (0, 210, 255)]
    }
]

# Modern UI / Glassmorphism Palette Defaults
COLOR_BG_DARK = (12, 10, 24)
COLOR_GLASS_BG = (22, 18, 42, 215)
COLOR_GLASS_BORDER = (0, 240, 255, 120)
COLOR_GLASS_HIGHLIGHT = (255, 255, 255, 30)

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
