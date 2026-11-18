import math
import random
import pygame
from src.settings import (
    GROUND_Y, SCREEN_WIDTH, COLOR_OBSTACLE_GROUND, COLOR_OBSTACLE_AIR
)

class Obstacle:
    TYPE_SMALL_GROUND = "small_ground"
    TYPE_LARGE_GROUND = "large_ground"
    TYPE_DOUBLE_GROUND = "double_ground"
    TYPE_FLYING_DRONE = "flying_drone"

    def __init__(self, obs_type, x_pos):
        self.type = obs_type
        self.x = x_pos
        self.anim_tick = random.randint(0, 100)

        if self.type == self.TYPE_SMALL_GROUND:
            self.width = 24
            self.height = 44
            self.y = GROUND_Y
        elif self.type == self.TYPE_LARGE_GROUND:
            self.width = 32
            self.height = 64
            self.y = GROUND_Y
        elif self.type == self.TYPE_DOUBLE_GROUND:
            self.width = 54
            self.height = 48
            self.y = GROUND_Y
        elif self.type == self.TYPE_FLYING_DRONE:
            self.width = 42
            self.height = 24
            # Placed so the player can duck under it (approx 35-50 px above ground)
            self.y = GROUND_Y - 38
        else:
            self.width = 30
            self.height = 40
            self.y = GROUND_Y

    @property
    def rect(self):
        # Slightly trimmed hitbox for fair gameplay
        if self.type == self.TYPE_FLYING_DRONE:
            return pygame.Rect(self.x + 3, self.y - self.height + 3, self.width - 6, self.height - 6)
        return pygame.Rect(self.x + 4, self.y - self.height + 4, self.width - 8, self.height - 4)

    def update(self, speed):
        self.x -= speed
        self.anim_tick += 1

    def is_offscreen(self):
        return self.x + self.width < -50

    def draw(self, surface):
        if self.type == self.TYPE_FLYING_DRONE:
            # Floating drone with pulsing wings/light
            top_y = self.y - self.height + int(math.sin(self.anim_tick * 0.15) * 4)
            # Body
            pygame.draw.rect(surface, COLOR_OBSTACLE_AIR, (self.x, top_y, self.width, self.height), border_radius=5)
            # Wings
            wing_flap = int(math.sin(self.anim_tick * 0.4) * 6)
            pygame.draw.line(surface, (255, 230, 150), (self.x + 4, top_y + 4), (self.x - 8, top_y - 4 + wing_flap), 3)
            pygame.draw.line(surface, (255, 230, 150), (self.x + self.width - 4, top_y + 4), (self.x + self.width + 8, top_y - 4 + wing_flap), 3)
            # Glowing core
            pygame.draw.circle(surface, (255, 255, 255), (int(self.x + self.width // 2), int(top_y + self.height // 2)), 4)
        else:
            # Ground Spikes / Cyber Cacti
            top_y = self.y - self.height
            pygame.draw.rect(surface, COLOR_OBSTACLE_GROUND, (self.x, top_y, self.width, self.height), border_radius=4)
            # Inner neon lines
            inner_rect = pygame.Rect(self.x + 4, top_y + 4, self.width - 8, self.height - 6)
            pygame.draw.rect(surface, (255, 120, 160), inner_rect, border_radius=2)
            # Spikes on top
            num_spikes = max(2, self.width // 10)
            step = self.width / num_spikes
            for i in range(num_spikes):
                sx = self.x + i * step + step / 2
                pygame.draw.polygon(surface, (255, 200, 220), [
                    (sx - 3, top_y),
                    (sx + 3, top_y),
                    (sx, top_y - 6)
                ])
