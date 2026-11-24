import math
import random
import pygame
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_Y, STAGES
)

class Background:
    def __init__(self):
        self.ground_offset = 0
        self.stars = [
            (random.randint(0, SCREEN_WIDTH), random.randint(15, GROUND_Y - 90), random.choice([1, 2]), random.random())
            for _ in range(45)
        ]
        # City skyline buildings (width, height, layer, windows pre-generated)
        self.buildings_back = self._generate_skyline(count=26, height_min=60, height_max=160, has_windows=False)
        self.buildings_front = self._generate_skyline(count=22, height_min=100, height_max=220, has_windows=True)
        self.back_scroll = 0
        self.front_scroll = 0

    def _generate_skyline(self, count, height_min, height_max, has_windows=False):
        buildings = []
        cur_x = 0
        for _ in range(count):
            w = random.randint(44, 84)
            h = random.randint(height_min, height_max)
            windows = []
            if has_windows:
                # Pre-generate permanent static window positions relative to building origin
                # Completely eliminates flickering as buildings move!
                for rel_y in range(14, h - 22, 24):
                    for rel_x in range(8, w - 12, 16):
                        # 65% of window bays are lit
                        if random.random() < 0.65:
                            win_w = 8
                            win_h = 12
                            # Window variant (0: primary, 1: secondary, 2: warm)
                            variant = random.choice([0, 1, 2])
                            windows.append((rel_x, rel_y, win_w, win_h, variant))
            buildings.append({
                'x': cur_x,
                'w': w,
                'h': h,
                'windows': windows
            })
            cur_x += w + random.randint(6, 22)
        return buildings

    def update(self, speed):
        self.ground_offset = (self.ground_offset + speed) % 40
        self.back_scroll = (self.back_scroll + speed * 0.15) % (SCREEN_WIDTH * 2)
        self.front_scroll = (self.front_scroll + speed * 0.38) % (SCREEN_WIDTH * 2)

    def draw(self, surface, stage=None):
        if stage is None:
            stage = STAGES[0]

        sky_top = stage["sky_top"]
        sky_bottom = stage["sky_bottom"]
        ground_color = stage["ground"]
        ground_line = stage["ground_line"]
        grid_color = stage["grid"]
        window_palette = stage.get("window_colors", [(0, 240, 255), (180, 230, 255), (255, 240, 150)])

        # 1. Gradient Sky
        # Draw sky gradient bands
        grad_steps = 14
        band_h = GROUND_Y // grad_steps
        for i in range(grad_steps):
            t = i / float(grad_steps)
            r = int(sky_top[0] + (sky_bottom[0] - sky_top[0]) * t)
            g = int(sky_top[1] + (sky_bottom[1] - sky_top[1]) * t)
            b = int(sky_top[2] + (sky_bottom[2] - sky_top[2]) * t)
            pygame.draw.rect(surface, (r, g, b), (0, i * band_h, SCREEN_WIDTH, band_h + 2))

        # 2. Twinkling Stars (Steady soft glow)
        for sx, sy, size, phase in self.stars:
            brightness = 190 + int(math.sin(pygame.time.get_ticks() * 0.002 + phase * 6.28) * 50)
            star_color = (brightness, brightness, min(255, brightness + 20))
            pygame.draw.circle(surface, star_color, (sx, sy), size)

        # 3. Distant Skyline (Back layer)
        for b in self.buildings_back:
            bx = (b['x'] - self.back_scroll * 1.5) % (SCREEN_WIDTH * 2) - 100
            if -100 <= bx <= SCREEN_WIDTH + 100:
                rect = pygame.Rect(bx, GROUND_Y - b['h'], b['w'], b['h'])
                back_col = (int(sky_bottom[0] * 0.8), int(sky_bottom[1] * 0.7), int(sky_bottom[2] * 0.9))
                pygame.draw.rect(surface, back_col, rect)

        # 4. Near Skyline (Front layer) with 100% Non-flickering Pre-generated Windows
        for b in self.buildings_front:
            bx = (b['x'] - self.front_scroll * 1.5) % (SCREEN_WIDTH * 2) - 100
            if -100 <= bx <= SCREEN_WIDTH + 100:
                b_top = GROUND_Y - b['h']
                rect = pygame.Rect(bx, b_top, b['w'], b['h'])
                front_col = (int(sky_bottom[0] * 1.1 + 8), int(sky_bottom[1] * 1.0 + 8), int(sky_bottom[2] * 1.1 + 14))
                pygame.draw.rect(surface, front_col, rect)
                
                # Roof border line
                pygame.draw.line(surface, (front_col[0] + 25, front_col[1] + 25, front_col[2] + 35), (bx, b_top), (bx + b['w'], b_top), 2)

                # Pre-generated, permanent static windows: NEVER flicker or blink!
                for rel_x, rel_y, ww, wh, variant in b.get('windows', []):
                    win_color = window_palette[variant % len(window_palette)]
                    win_rect = pygame.Rect(bx + rel_x, b_top + rel_y, ww, wh)
                    pygame.draw.rect(surface, win_color, win_rect)

        # 5. Ground fill
        ground_rect = pygame.Rect(0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y)
        pygame.draw.rect(surface, ground_color, ground_rect)

        # 6. Glowing Horizon Neon Line (Stage dynamic accent)
        pygame.draw.line(surface, ground_line, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 3)

        # 7. Scrolling Grid Stripes on ground (retro perspective feel)
        for x in range(-40, SCREEN_WIDTH + 40, 40):
            gx = x - int(self.ground_offset)
            pygame.draw.line(surface, grid_color, (gx, GROUND_Y), (gx - 30, SCREEN_HEIGHT), 2)
