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
            (random.randint(0, SCREEN_WIDTH), random.randint(15, GROUND_Y - 110), random.choice([1, 2]), random.random())
            for _ in range(50)
        ]

        # Drifting soft volumetric clouds
        self.clouds = [
            {'x': random.randint(0, SCREEN_WIDTH), 'y': random.randint(25, 120), 'w': random.randint(110, 180), 'speed': random.uniform(0.12, 0.28)}
            for _ in range(5)
        ]

        # City skyline buildings (width, height, layer, windows, billboard)
        self.buildings_back = self._generate_skyline(count=28, height_min=70, height_max=170, has_windows=False)
        self.buildings_front = self._generate_skyline(count=24, height_min=110, height_max=240, has_windows=True, has_billboards=True)
        self.back_scroll = 0
        self.front_scroll = 0

    def _generate_skyline(self, count, height_min, height_max, has_windows=False, has_billboards=False):
        buildings = []
        cur_x = 0
        billboard_texts = ["SUBWAY", "RUN", "NEON", "CYBER", "SURF"]

        for i in range(count):
            w = random.randint(48, 88)
            h = random.randint(height_min, height_max)
            windows = []
            billboard = None

            if has_windows:
                # Pre-generate permanent static window bays
                for rel_y in range(16, h - 24, 24):
                    for rel_x in range(8, w - 12, 16):
                        if random.random() < 0.65:
                            windows.append((rel_x, rel_y, 8, 12, random.choice([0, 1, 2])))

            if has_billboards and random.random() < 0.25 and w >= 55:
                billboard = {
                    'text': billboard_texts[i % len(billboard_texts)],
                    'w': w - 12,
                    'h': 18
                }

            buildings.append({
                'x': cur_x,
                'w': w,
                'h': h,
                'windows': windows,
                'billboard': billboard
            })
            cur_x += w + random.randint(6, 20)
        return buildings

    def update(self, speed):
        self.ground_offset = (self.ground_offset + speed) % 40
        self.back_scroll = (self.back_scroll + speed * 0.15) % (SCREEN_WIDTH * 2)
        self.front_scroll = (self.front_scroll + speed * 0.38) % (SCREEN_WIDTH * 2)

        # Update drifting clouds
        for c in self.clouds:
            c['x'] -= c['speed'] * (speed / 7.0 + 0.3)
            if c['x'] + c['w'] < -50:
                c['x'] = SCREEN_WIDTH + random.randint(20, 100)
                c['y'] = random.randint(25, 120)

    def draw(self, surface, stage=None):
        if stage is None:
            stage = STAGES[0]

        sky_top = stage["sky_top"]
        sky_bottom = stage["sky_bottom"]
        ground_color = stage["ground"]
        ground_line = stage["ground_line"]
        grid_color = stage["grid"]
        moon_col = stage.get("moon_color", (220, 245, 255))
        window_palette = stage.get("window_colors", [(0, 240, 255), (180, 230, 255), (255, 240, 150)])

        # 1. Sky Gradient
        grad_steps = 16
        band_h = GROUND_Y // grad_steps
        for i in range(grad_steps):
            t = i / float(grad_steps)
            r = int(sky_top[0] + (sky_bottom[0] - sky_top[0]) * t)
            g = int(sky_top[1] + (sky_bottom[1] - sky_top[1]) * t)
            b = int(sky_top[2] + (sky_bottom[2] - sky_top[2]) * t)
            pygame.draw.rect(surface, (r, g, b), (0, i * band_h, SCREEN_WIDTH, band_h + 2))

        # 2. Celestial Moon / Cyber Sun with Atmospheric Halos
        moon_x, moon_y = SCREEN_WIDTH - 180, 110
        # Multi-layered soft glow halos
        for halo_r, alpha in [(65, 18), (52, 35), (42, 60)]:
            halo_surf = pygame.Surface((halo_r * 2, halo_r * 2), pygame.SRCALPHA)
            pygame.draw.circle(halo_surf, (moon_col[0], moon_col[1], moon_col[2], alpha), (halo_r, halo_r), halo_r)
            surface.blit(halo_surf, (moon_x - halo_r, moon_y - halo_r))
        # Solid moon core
        pygame.draw.circle(surface, moon_col, (moon_x, moon_y), 32)
        # Subtle crater details
        pygame.draw.circle(surface, (int(moon_col[0] * 0.9), int(moon_col[1] * 0.9), int(moon_col[2] * 0.95)), (moon_x - 10, moon_y - 6), 6)
        pygame.draw.circle(surface, (int(moon_col[0] * 0.92), int(moon_col[1] * 0.92), int(moon_col[2] * 0.96)), (moon_x + 8, moon_y + 10), 8)

        # 3. Twinkling Stars
        for sx, sy, size, phase in self.stars:
            brightness = 190 + int(math.sin(pygame.time.get_ticks() * 0.002 + phase * 6.28) * 55)
            pygame.draw.circle(surface, (brightness, brightness, min(255, brightness + 20)), (sx, sy), size)

        # 4. Volumetric Drifting Clouds
        for c in self.clouds:
            cloud_surf = pygame.Surface((c['w'], 35), pygame.SRCALPHA)
            pygame.draw.ellipse(cloud_surf, (255, 255, 255, 22), (0, 6, c['w'], 24))
            pygame.draw.ellipse(cloud_surf, (255, 255, 255, 30), (c['w'] * 0.2, 0, c['w'] * 0.6, 28))
            surface.blit(cloud_surf, (int(c['x']), int(c['y'])))

        # 5. Distant Skyline (Back layer)
        for b in self.buildings_back:
            bx = (b['x'] - self.back_scroll * 1.5) % (SCREEN_WIDTH * 2) - 100
            if -100 <= bx <= SCREEN_WIDTH + 100:
                rect = pygame.Rect(bx, GROUND_Y - b['h'], b['w'], b['h'])
                back_col = (int(sky_bottom[0] * 0.75), int(sky_bottom[1] * 0.65), int(sky_bottom[2] * 0.85))
                pygame.draw.rect(surface, back_col, rect)

        # 6. Near Skyline (Front layer) with Billboards & Permanent Non-flickering Windows
        for b in self.buildings_front:
            bx = (b['x'] - self.front_scroll * 1.5) % (SCREEN_WIDTH * 2) - 100
            if -100 <= bx <= SCREEN_WIDTH + 100:
                b_top = GROUND_Y - b['h']
                rect = pygame.Rect(bx, b_top, b['w'], b['h'])
                front_col = (int(sky_bottom[0] * 1.05 + 10), int(sky_bottom[1] * 0.95 + 10), int(sky_bottom[2] * 1.1 + 16))
                pygame.draw.rect(surface, front_col, rect)
                
                # Rooftop antenna / ledge
                pygame.draw.line(surface, (front_col[0] + 30, front_col[1] + 30, front_col[2] + 45), (bx, b_top), (bx + b['w'], b_top), 2)
                if b['w'] > 65:
                    pygame.draw.line(surface, (255, 75, 95), (bx + b['w'] // 2, b_top), (bx + b['w'] // 2, b_top - 12), 2)
                    pygame.draw.circle(surface, (255, 255, 255), (bx + b['w'] // 2, b_top - 13), 2)

                # Holographic Rooftop Billboard (if present)
                if b.get('billboard'):
                    bb = b['billboard']
                    bb_rect = pygame.Rect(bx + 6, b_top + 8, bb['w'], bb['h'])
                    pygame.draw.rect(surface, (16, 12, 28), bb_rect, border_radius=3)
                    pygame.draw.rect(surface, ground_line, bb_rect, 1, border_radius=3)
                    font_bb = pygame.font.SysFont("Consolas", 11, bold=True)
                    txt_surf = font_bb.render(bb['text'], True, ground_line)
                    surface.blit(txt_surf, (bb_rect.centerx - txt_surf.get_width() // 2, bb_rect.centery - txt_surf.get_height() // 2))

                # Windows (Permanent pre-generated positions - 100% steady, NO FLICKER)
                for rel_x, rel_y, ww, wh, variant in b.get('windows', []):
                    # Skip windows if overlapping billboard
                    if b.get('billboard') and rel_y < 32:
                        continue
                    win_color = window_palette[variant % len(window_palette)]
                    pygame.draw.rect(surface, win_color, (bx + rel_x, b_top + rel_y, ww, wh))

        # 7. Ground fill
        ground_rect = pygame.Rect(0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y)
        pygame.draw.rect(surface, ground_color, ground_rect)

        # 8. Subway Railway Track Ties & Metallic Rails
        # Upper rail
        pygame.draw.line(surface, (140, 150, 180), (0, GROUND_Y - 2), (SCREEN_WIDTH, GROUND_Y - 2), 2)
        # Glowing Horizon Line
        pygame.draw.line(surface, ground_line, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 3)
        # Lower rail
        pygame.draw.line(surface, (100, 110, 140), (0, GROUND_Y + 12), (SCREEN_WIDTH, GROUND_Y + 12), 2)

        # Cross Ties / Sleepers (moving with ground offset)
        for x in range(-40, SCREEN_WIDTH + 40, 36):
            rx = x - int(self.ground_offset)
            pygame.draw.line(surface, (60, 50, 75), (rx, GROUND_Y), (rx - 4, GROUND_Y + 12), 4)

        # 9. Scrolling Perspective Grid (Subway yard road lines)
        for x in range(-40, SCREEN_WIDTH + 40, 40):
            gx = x - int(self.ground_offset)
            pygame.draw.line(surface, grid_color, (gx, GROUND_Y + 12), (gx - 32, SCREEN_HEIGHT), 2)
