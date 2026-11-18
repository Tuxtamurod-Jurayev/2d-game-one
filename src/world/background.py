import math
import random
import pygame
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_Y,
    COLOR_BG_DARK, COLOR_SKY_TOP, COLOR_SKY_BOTTOM,
    COLOR_GROUND, COLOR_GROUND_LINE, COLOR_GRID
)

class Background:
    def __init__(self):
        self.ground_offset = 0
        self.stars = [
            (random.randint(0, SCREEN_WIDTH), random.randint(20, GROUND_Y - 80), random.choice([1, 2]), random.random())
            for _ in range(40)
        ]
        # City skyline buildings (width, height, layer)
        self.buildings_back = self._generate_skyline(count=25, height_min=60, height_max=160)
        self.buildings_front = self._generate_skyline(count=20, height_min=100, height_max=220)
        self.back_scroll = 0
        self.front_scroll = 0

    def _generate_skyline(self, count, height_min, height_max):
        buildings = []
        cur_x = 0
        for _ in range(count):
            w = random.randint(40, 80)
            h = random.randint(height_min, height_max)
            buildings.append({'x': cur_x, 'w': w, 'h': h})
            cur_x += w + random.randint(5, 20)
        return buildings

    def update(self, speed):
        self.ground_offset = (self.ground_offset + speed) % 40
        self.back_scroll = (self.back_scroll + speed * 0.15) % SCREEN_WIDTH
        self.front_scroll = (self.front_scroll + speed * 0.4) % SCREEN_WIDTH

    def draw(self, surface):
        # 1. Gradient Sky
        surface.fill(COLOR_BG_DARK)
        
        # 2. Twinkling Stars
        for sx, sy, size, phase in self.stars:
            brightness = 180 + int(math.sin(pygame.time.get_ticks() * 0.003 + phase * 6.28) * 60)
            star_color = (brightness, brightness, min(255, brightness + 20))
            pygame.draw.circle(surface, star_color, (sx, sy), size)

        # 3. Distant Skyline (Back layer)
        for b in self.buildings_back:
            bx = (b['x'] - self.back_scroll * 1.5) % (SCREEN_WIDTH * 2) - 100
            if -100 <= bx <= SCREEN_WIDTH + 100:
                rect = pygame.Rect(bx, GROUND_Y - b['h'], b['w'], b['h'])
                pygame.draw.rect(surface, (28, 22, 50), rect)

        # 4. Near Skyline (Front layer)
        for b in self.buildings_front:
            bx = (b['x'] - self.front_scroll * 1.5) % (SCREEN_WIDTH * 2) - 100
            if -100 <= bx <= SCREEN_WIDTH + 100:
                rect = pygame.Rect(bx, GROUND_Y - b['h'], b['w'], b['h'])
                pygame.draw.rect(surface, (40, 30, 68), rect)
                # Glowing windows
                for wy in range(GROUND_Y - b['h'] + 10, GROUND_Y - 20, 25):
                    for wx in range(int(bx) + 8, int(bx) + b['w'] - 12, 18):
                        if (wx + wy) % 3 == 0:
                            pygame.draw.rect(surface, (255, 220, 100), (wx, wy, 8, 12))

        # 5. Ground fill
        ground_rect = pygame.Rect(0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y)
        pygame.draw.rect(surface, COLOR_GROUND, ground_rect)

        # 6. Glowing Horizon Neon Line
        pygame.draw.line(surface, COLOR_GROUND_LINE, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 3)

        # 7. Scrolling Grid Stripes on ground (retro perspective feel)
        for x in range(-40, SCREEN_WIDTH + 40, 40):
            gx = x - int(self.ground_offset)
            pygame.draw.line(surface, COLOR_GRID, (gx, GROUND_Y), (gx - 30, SCREEN_HEIGHT), 2)
