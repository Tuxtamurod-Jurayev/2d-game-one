import math
import random
import pygame
from src.settings import (
    PLAYER_X, GROUND_Y, GRAVITY, JUMP_STRENGTH,
    COLOR_PLAYER, COLOR_PLAYER_DUCK, COLOR_PLAYER_EYE
)

class Particle:
    def __init__(self, x, y, vx, vy, color, size, lifetime):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.age = 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.age += 1
        self.size = max(0, self.size - 0.1)

    def is_alive(self):
        return self.age < self.lifetime and self.size > 0

    def draw(self, surface):
        alpha_factor = 1.0 - (self.age / self.lifetime)
        s = int(self.size)
        if s > 0:
            pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), s, s))

class Player:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = PLAYER_X
        self.y = GROUND_Y
        self.vy = 0
        self.is_grounded = True
        self.is_ducking = False
        self.width_normal = 38
        self.height_normal = 52
        self.width_duck = 54
        self.height_duck = 26
        
        self.run_timer = 0
        self.particles = []
        self.is_alive = True

    @property
    def current_width(self):
        return self.width_duck if self.is_ducking else self.width_normal

    @property
    def current_height(self):
        return self.height_duck if self.is_ducking else self.height_normal

    @property
    def rect(self):
        # Slightly shrink hitbox for player-friendly collision feel
        w = self.current_width
        h = self.current_height
        return pygame.Rect(self.x - w // 2 + 4, self.y - h + 4, w - 8, h - 6)

    def jump(self, sound_mgr):
        if self.is_grounded and not self.is_ducking:
            self.vy = JUMP_STRENGTH
            self.is_grounded = False
            sound_mgr.play_jump()
            # Spawn jump puff particles
            for _ in range(8):
                self.particles.append(Particle(
                    self.x + random.randint(-15, 15),
                    self.y - 2,
                    random.uniform(-2, 2),
                    random.uniform(-1.5, -0.2),
                    (180, 180, 210),
                    random.uniform(4, 7),
                    lifetime=20
                ))

    def update(self, keys_pressed):
        # Duck control
        if self.is_grounded:
            if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
                self.is_ducking = True
            else:
                self.is_ducking = False
        else:
            # Fast fall if holding down in mid-air
            if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
                self.vy += GRAVITY * 1.5

        # Gravity & vertical movement
        self.vy += GRAVITY
        self.y += self.vy

        if self.y >= GROUND_Y:
            self.y = GROUND_Y
            self.vy = 0
            self.is_grounded = True

        # Running particles
        self.run_timer += 1
        if self.is_grounded and self.run_timer % 6 == 0:
            self.particles.append(Particle(
                self.x - self.current_width // 2,
                self.y - 3,
                random.uniform(-3, -1),
                random.uniform(-1, 0),
                (140, 130, 170),
                random.uniform(3, 5),
                lifetime=15
            ))

        # Update particles
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.is_alive()]

    def draw(self, surface):
        # Draw trailing particles
        for p in self.particles:
            p.draw(surface)

        w = self.current_width
        h = self.current_height
        top_left_x = self.x - w // 2
        top_left_y = self.y - h

        # Slight bobbing motion while running
        bob_offset = 0
        if self.is_grounded and not self.is_ducking:
            bob_offset = int(math.sin(self.run_timer * 0.35) * 3)

        color = COLOR_PLAYER_DUCK if self.is_ducking else COLOR_PLAYER

        # Body (rounded pixel style)
        draw_rect = pygame.Rect(top_left_x, top_left_y + bob_offset, w, h - bob_offset)
        pygame.draw.rect(surface, color, draw_rect, border_radius=6)

        # Inner visor / glowing eye
        eye_y = top_left_y + bob_offset + (6 if self.is_ducking else 10)
        eye_rect = pygame.Rect(top_left_x + w - 14, eye_y, 10, 8)
        pygame.draw.rect(surface, COLOR_PLAYER_EYE, eye_rect, border_radius=3)
        # Pupil
        pygame.draw.rect(surface, (20, 20, 40), (top_left_x + w - 8, eye_y + 2, 3, 4))

        # Legs animation if grounded
        if self.is_grounded and not self.is_ducking:
            leg_swing = math.sin(self.run_timer * 0.35) * 6
            # Back leg
            pygame.draw.rect(surface, (0, 180, 140), (self.x - 10 - leg_swing, self.y - 6, 6, 6), border_radius=2)
            # Front leg
            pygame.draw.rect(surface, (0, 255, 180), (self.x + 4 + leg_swing, self.y - 6, 6, 6), border_radius=2)
