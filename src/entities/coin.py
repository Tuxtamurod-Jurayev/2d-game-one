import math
import random
import pygame
from src.settings import COLOR_COIN

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12
        self.anim_tick = random.randint(0, 100)
        self.collected = False

    @property
    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self, speed):
        self.x -= speed
        self.anim_tick += 1

    def is_offscreen(self):
        return self.x + self.radius < -50

    def draw(self, surface):
        bob_y = self.y + math.sin(self.anim_tick * 0.1) * 5
        # Gold outer circle
        pygame.draw.circle(surface, COLOR_COIN, (int(self.x), int(bob_y)), self.radius)
        # Inner highlight
        pygame.draw.circle(surface, (255, 255, 200), (int(self.x - 3), int(bob_y - 3)), 3)
        # Inner border
        pygame.draw.circle(surface, (210, 160, 0), (int(self.x), int(bob_y)), self.radius - 3, 2)
