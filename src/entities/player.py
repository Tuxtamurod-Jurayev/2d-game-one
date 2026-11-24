"""
Humanoid Athletic Runner Entity with Progressive Multi-Jump (Double Jump).
Features:
- Anatomically accurate proportions (Head, Hair with wind dynamics, Torso/Jacket, Dual-jointed Limbs).
- Double Jump system: 1st jump from ground + 2nd higher jump in mid-air with acrobatic aerial flip.
- Dynamic shockwave ring particles and landing impact effects.
- Variable jump height (cut jump when button released early).
- Low-profile sliding pose for dodging aerial drones.
"""
import math
import random
import pygame
from src.settings import (
    PLAYER_X, GROUND_Y, GRAVITY, JUMP_STRENGTH, DOUBLE_JUMP_STRENGTH,
    SKIN_TONE, SKIN_SHADOW, HAIR_COLOR, HAIR_HIGHLIGHT,
    CLOTH_SHIRT, CLOTH_SHIRT_ACCENT, CLOTH_PANTS,
    CLOTH_SHOES, CLOTH_SHOES_SOLES
)

class Particle:
    def __init__(self, x, y, vx, vy, color, size, lifetime, decay_rate=0.1, is_ring=False):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.decay_rate = decay_rate
        self.is_ring = is_ring
        self.age = 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.age += 1
        if self.is_ring:
            self.size += 1.5  # Expands outward
        else:
            self.size = max(0, self.size - self.decay_rate)

    def is_alive(self):
        return self.age < self.lifetime and self.size > 0

    def draw(self, surface):
        if self.size > 0:
            if self.is_ring:
                alpha = max(0, int(255 * (1.0 - self.age / self.lifetime)))
                ring_surf = pygame.Surface((int(self.size * 2 + 4), int(self.size * 0.8 + 4)), pygame.SRCALPHA)
                ring_color = (self.color[0], self.color[1], self.color[2], alpha)
                pygame.draw.ellipse(ring_surf, ring_color, (2, 2, int(self.size * 2), int(self.size * 0.8)), 2)
                surface.blit(ring_surf, (int(self.x - self.size), int(self.y - self.size * 0.4)))
            else:
                pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))


class Player:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = PLAYER_X
        self.y = GROUND_Y
        self.vy = 0
        self.is_grounded = True
        self.is_ducking = False

        # Multi-jump system (Ground Jump + Double Jump)
        self.jump_count = 0
        self.max_jumps = 2
        self.is_double_jumping = False
        self.flip_angle = 0.0

        # Hitbox dimensions
        self.width_normal = 32
        self.height_normal = 58
        self.width_duck = 56
        self.height_duck = 28

        self.anim_tick = 0
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
        w = self.current_width
        h = self.current_height
        if self.is_ducking:
            return pygame.Rect(self.x - 24, self.y - h + 2, w - 8, h - 4)
        return pygame.Rect(self.x - 14, self.y - h + 4, w - 4, h - 6)

    def jump(self, sound_mgr):
        """Performs 1st ground jump or 2nd higher double-jump."""
        if self.is_ducking:
            return

        if self.is_grounded:
            # First Jump from Ground
            self.vy = JUMP_STRENGTH
            self.is_grounded = False
            self.jump_count = 1
            self.is_double_jumping = False
            sound_mgr.play_jump()

            # Liftoff dust burst
            for _ in range(9):
                self.particles.append(Particle(
                    self.x + random.uniform(-10, 10),
                    self.y - 2,
                    random.uniform(-3, 1),
                    random.uniform(-2, -0.2),
                    (180, 190, 220),
                    random.uniform(4, 7),
                    lifetime=20,
                    decay_rate=0.25
                ))

        elif self.jump_count < self.max_jumps:
            # Second Jump in Mid-Air (DOUBLE JUMP - Balandroq sakrash)
            self.vy = DOUBLE_JUMP_STRENGTH
            self.jump_count = 2
            self.is_double_jumping = True
            self.flip_angle = 0.0
            sound_mgr.play_double_jump()

            # Shockwave energy ring expanding under player
            self.particles.append(Particle(
                self.x, self.y - 8,
                0, 0,
                (0, 240, 255),
                size=8,
                lifetime=22,
                is_ring=True
            ))

            # Double jump energetic spark shower
            for _ in range(12):
                self.particles.append(Particle(
                    self.x + random.uniform(-6, 6),
                    self.y - 6,
                    random.uniform(-3.5, 3.5),
                    random.uniform(-1, 3.0),
                    random.choice([(0, 240, 255), (180, 255, 240), (255, 255, 255)]),
                    random.uniform(3, 5),
                    lifetime=18,
                    decay_rate=0.22
                ))

    def cut_jump(self):
        """Allows variable jump height: releasing button early cuts vertical speed."""
        if not self.is_grounded and self.vy < -4.5:
            self.vy *= 0.55

    def update(self, keys_pressed, speed_factor=1.0):
        # 1. Slide / Duck control
        if self.is_grounded:
            if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
                self.is_ducking = True
            else:
                self.is_ducking = False
        else:
            # Fast-fall dive if holding DOWN in mid-air
            if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
                self.vy += GRAVITY * 1.6

        # 2. Gravity & Physics
        self.vy += GRAVITY
        self.y += self.vy

        # 3. Ground Collision & Landing
        if self.y >= GROUND_Y:
            if not self.is_grounded:
                # Landing footstep dust poof
                for _ in range(7):
                    self.particles.append(Particle(
                        self.x + random.uniform(-8, 8),
                        GROUND_Y - 2,
                        random.uniform(-2.5, 2.5),
                        random.uniform(-1.5, -0.2),
                        (190, 200, 230),
                        random.uniform(3, 5),
                        lifetime=16
                    ))
            self.y = GROUND_Y
            self.vy = 0
            self.is_grounded = True
            self.jump_count = 0
            self.is_double_jumping = False
            self.flip_angle = 0.0

        # 4. Double Jump Somersault Rotation
        if self.is_double_jumping and not self.is_grounded:
            self.flip_angle += 22.0
            if self.flip_angle >= 360.0:
                self.flip_angle = 0.0
                self.is_double_jumping = False

        # 5. Animation cycle progression
        step_rate = 0.28 * (speed_factor / 7.0)
        self.anim_tick += step_rate

        # 6. Particles (Footstep dust or slide sparks)
        if self.is_grounded:
            if self.is_ducking:
                if random.random() < 0.7:
                    self.particles.append(Particle(
                        self.x - 12 + random.uniform(-5, 5),
                        self.y - 2,
                        random.uniform(-4, -1),
                        random.uniform(-1.5, 0),
                        random.choice([(0, 240, 255), (255, 180, 50), (255, 255, 255)]),
                        random.uniform(3, 5),
                        lifetime=14,
                        decay_rate=0.25
                    ))
            else:
                if int(self.anim_tick * 2) % 4 == 0:
                    self.particles.append(Particle(
                        self.x - 10,
                        self.y - 2,
                        random.uniform(-3, -1),
                        random.uniform(-1, 0),
                        (140, 130, 165),
                        random.uniform(3, 5),
                        lifetime=14
                    ))

        # Update active particles
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.is_alive()]

    def draw(self, surface):
        # 1. Ground Shadow (shrinks when player jumps high)
        altitude = max(0, GROUND_Y - self.y)
        shadow_scale = max(0.2, 1.0 - (altitude / 260.0))
        shadow_w = int(28 * shadow_scale)
        shadow_h = int(8 * shadow_scale)
        shadow_surf = pygame.Surface((shadow_w * 2, shadow_h * 2), pygame.SRCALPHA)
        shadow_alpha = int(90 * shadow_scale)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, shadow_alpha), (0, 0, shadow_w * 2, shadow_h * 2))
        surface.blit(shadow_surf, (self.x - shadow_w, GROUND_Y - shadow_h // 2))

        # 2. Draw particles (behind character)
        for p in self.particles:
            p.draw(surface)

        # 3. Draw Character by State
        if self.is_ducking:
            self._draw_sliding_human(surface)
        elif not self.is_grounded:
            if self.is_double_jumping:
                self._draw_double_jump_somersault(surface)
            else:
                self._draw_jumping_human(surface)
        else:
            self._draw_running_human(surface)

    def _draw_double_jump_somersault(self, surface):
        """Draws dynamic 360-degree athletic somersault flip during double jump."""
        # Render runner to temporary surface and rotate it smoothly
        temp_w, temp_h = 70, 70
        temp_surf = pygame.Surface((temp_w, temp_h), pygame.SRCALPHA)
        center_x, center_y = temp_w // 2, temp_h // 2

        # Draw curled athletic body in center of temp surface
        # Torso
        pygame.draw.rect(temp_surf, CLOTH_SHIRT, (center_x - 8, center_y - 10, 16, 18), border_radius=4)
        pygame.draw.line(temp_surf, (0, 240, 255), (center_x - 6, center_y - 7), (center_x - 6, center_y + 5), 2)
        # Head
        pygame.draw.circle(temp_surf, SKIN_TONE, (center_x + 4, center_y - 18), 8)
        pygame.draw.polygon(temp_surf, HAIR_COLOR, [
            (center_x - 4, center_y - 16),
            (center_x - 8, center_y - 25),
            (center_x + 8, center_y - 24),
            (center_x + 10, center_y - 18)
        ])
        # Curled legs
        pygame.draw.line(temp_surf, CLOTH_PANTS, (center_x - 4, center_y + 4), (center_x + 8, center_y + 14), 6)
        pygame.draw.line(temp_surf, CLOTH_PANTS, (center_x + 8, center_y + 14), (center_x - 2, center_y + 18), 5)
        # Sneaker
        pygame.draw.rect(temp_surf, CLOTH_SHOES, (center_x - 4, center_y + 16, 9, 5), border_radius=2)
        # Arm holding tuck
        pygame.draw.line(temp_surf, CLOTH_SHIRT, (center_x - 4, center_y - 4), (center_x + 6, center_y + 6), 4)

        # Rotate surface
        rotated = pygame.transform.rotate(temp_surf, -self.flip_angle)
        new_rect = rotated.get_rect(center=(self.x, self.y - 28))
        surface.blit(rotated, new_rect.topleft)

        # Cyan double-jump aura trail
        trail_surf = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(trail_surf, (0, 240, 255, 70), (12, 12), 11, 2)
        surface.blit(trail_surf, (self.x - 12, self.y - 40))

    def _draw_running_human(self, surface):
        """Draws human runner with multi-joint limbs and torso bounce."""
        cycle = self.anim_tick
        bob = math.sin(cycle * 2.0) * 2.5
        lean = 4.0

        hip_x = self.x
        hip_y = self.y - 28 + bob

        leg1_angle = math.sin(cycle) * 0.75
        leg2_angle = math.sin(cycle + math.pi) * 0.75

        # --- A. BACK ARM ---
        arm_back_angle = -leg1_angle * 0.8
        self._draw_human_arm(surface, hip_x - 2, hip_y - 14, arm_back_angle, is_back=True)

        # --- B. BACK LEG ---
        self._draw_human_leg(surface, hip_x - 3, hip_y, leg2_angle, is_back=True)

        # --- C. TORSO & JACKET ---
        torso_w, torso_h = 16, 20
        torso_rect = pygame.Rect(hip_x - 8 + int(lean * 0.4), hip_y - torso_h, torso_w, torso_h)
        pygame.draw.rect(surface, CLOTH_SHIRT, torso_rect, border_radius=4)
        pygame.draw.line(surface, CLOTH_SHIRT_ACCENT, (torso_rect.centerx, torso_rect.top + 3), (torso_rect.centerx - 1, torso_rect.bottom - 2), 2)
        pygame.draw.line(surface, (0, 240, 255), (torso_rect.left + 2, torso_rect.top + 4), (torso_rect.left + 2, torso_rect.bottom - 4), 2)

        # --- D. HEAD, FACE & HAIR ---
        head_x = hip_x + int(lean)
        head_y = hip_y - torso_h - 11
        pygame.draw.rect(surface, SKIN_SHADOW, (head_x - 3, head_y + 9, 6, 4))
        pygame.draw.circle(surface, SKIN_TONE, (head_x, head_y), 9)
        pygame.draw.rect(surface, (255, 255, 255), (head_x + 3, head_y - 2, 4, 3))
        pygame.draw.rect(surface, (20, 20, 40), (head_x + 5, head_y - 2, 2, 3))
        pygame.draw.line(surface, HAIR_COLOR, (head_x + 2, head_y - 4), (head_x + 7, head_y - 4), 2)

        hair_flutter = math.sin(cycle * 3.0) * 2
        hair_points = [
            (head_x - 8, head_y + 1),
            (head_x - 9, head_y - 9),
            (head_x + 6, head_y - 10),
            (head_x + 8, head_y - 5),
            (head_x - 3, head_y - 3),
            (head_x - 12 + int(hair_flutter), head_y - 3)
        ]
        pygame.draw.polygon(surface, HAIR_COLOR, hair_points)
        pygame.draw.line(surface, HAIR_HIGHLIGHT, (head_x - 6, head_y - 8), (head_x + 4, head_y - 8), 2)

        # --- E. FRONT LEG ---
        self._draw_human_leg(surface, hip_x + 3, hip_y, leg1_angle, is_back=False)

        # --- F. FRONT ARM ---
        arm_front_angle = -leg2_angle * 0.8
        self._draw_human_arm(surface, hip_x + 2, hip_y - 14, arm_front_angle, is_back=False)

    def _draw_jumping_human(self, surface):
        """Draws athletic mid-air jump silhouette."""
        hip_x = self.x
        hip_y = self.y - 26

        self._draw_human_arm(surface, hip_x - 4, hip_y - 14, angle=-1.1, is_back=True)
        self._draw_human_leg(surface, hip_x - 4, hip_y, angle=-0.5, is_back=True, bend_knee=0.8)

        torso_rect = pygame.Rect(hip_x - 8, hip_y - 20, 16, 20)
        pygame.draw.rect(surface, CLOTH_SHIRT, torso_rect, border_radius=4)
        pygame.draw.line(surface, (0, 240, 255), (torso_rect.left + 2, torso_rect.top + 3), (torso_rect.left + 2, torso_rect.bottom - 3), 2)

        head_x = hip_x + 2
        head_y = hip_y - 31
        pygame.draw.rect(surface, SKIN_SHADOW, (head_x - 3, head_y + 9, 6, 4))
        pygame.draw.circle(surface, SKIN_TONE, (head_x, head_y), 9)
        pygame.draw.rect(surface, (255, 255, 255), (head_x + 3, head_y - 2, 4, 3))
        pygame.draw.rect(surface, (20, 20, 40), (head_x + 5, head_y - 2, 2, 3))

        hair_points = [
            (head_x - 8, head_y + 2),
            (head_x - 12, head_y - 12),
            (head_x + 5, head_y - 11),
            (head_x + 8, head_y - 5),
            (head_x - 3, head_y - 3)
        ]
        pygame.draw.polygon(surface, HAIR_COLOR, hair_points)

        self._draw_human_leg(surface, hip_x + 3, hip_y, angle=0.6, is_back=False, bend_knee=1.2)
        self._draw_human_arm(surface, hip_x + 3, hip_y - 14, angle=1.0, is_back=False)

    def _draw_sliding_human(self, surface):
        """Draws human in a low slide posture."""
        slide_y = self.y - 10
        slide_x = self.x

        torso_rect = pygame.Rect(slide_x - 18, slide_y - 14, 22, 14)
        pygame.draw.rect(surface, CLOTH_SHIRT, torso_rect, border_radius=4)

        head_x = slide_x - 22
        head_y = slide_y - 14
        pygame.draw.circle(surface, SKIN_TONE, (head_x, head_y), 8)
        pygame.draw.rect(surface, (255, 255, 255), (head_x + 2, head_y - 1, 3, 2))
        pygame.draw.rect(surface, (20, 20, 40), (head_x + 3, head_y - 1, 2, 2))
        pygame.draw.polygon(surface, HAIR_COLOR, [
            (head_x - 7, head_y + 1),
            (head_x - 14, head_y - 7),
            (head_x + 2, head_y - 8),
            (head_x + 6, head_y - 3)
        ])

        front_leg_points = [
            (slide_x + 2, slide_y - 4),
            (slide_x + 22, slide_y - 2),
            (slide_x + 30, slide_y - 1)
        ]
        pygame.draw.lines(surface, CLOTH_PANTS, False, front_leg_points, 6)
        pygame.draw.rect(surface, CLOTH_SHOES, (slide_x + 24, slide_y - 4, 12, 6), border_radius=2)
        pygame.draw.rect(surface, CLOTH_SHOES_SOLES, (slide_x + 24, slide_y + 1, 12, 2))

        pygame.draw.line(surface, (20, 25, 40), (slide_x - 8, slide_y - 4), (slide_x + 6, slide_y + 1), 6)
        pygame.draw.line(surface, SKIN_TONE, (slide_x - 6, slide_y - 8), (slide_x - 2, slide_y + 2), 4)

    def _draw_human_leg(self, surface, hip_x, hip_y, angle, is_back=False, bend_knee=None):
        thigh_len = 14
        shin_len = 14

        if bend_knee is None:
            knee_bend = math.sin(angle) * 0.4 if angle > 0 else -math.sin(angle) * 0.8
        else:
            knee_bend = bend_knee

        knee_x = hip_x + math.sin(angle) * thigh_len
        knee_y = hip_y + math.cos(angle) * thigh_len

        foot_angle = angle - knee_bend * 0.5
        foot_x = knee_x + math.sin(foot_angle) * shin_len
        foot_y = min(knee_y + math.cos(foot_angle) * shin_len, GROUND_Y)

        pants_color = (25, 28, 42) if is_back else CLOTH_PANTS
        shoe_color = (200, 50, 75) if is_back else CLOTH_SHOES

        pygame.draw.line(surface, pants_color, (hip_x, hip_y), (knee_x, knee_y), 6)
        pygame.draw.line(surface, pants_color, (knee_x, knee_y), (foot_x, foot_y), 5)

        shoe_w, shoe_h = 10, 6
        pygame.draw.rect(surface, shoe_color, (foot_x - 3, foot_y - shoe_h, shoe_w, shoe_h), border_radius=2)
        pygame.draw.rect(surface, CLOTH_SHOES_SOLES, (foot_x - 3, foot_y - 2, shoe_w, 2))

    def _draw_human_arm(self, surface, shoulder_x, shoulder_y, angle, is_back=False):
        arm_len = 11
        forearm_len = 10

        elbow_angle = angle + 0.35
        elbow_x = shoulder_x + math.sin(angle) * arm_len
        elbow_y = shoulder_y + math.cos(angle) * arm_len

        hand_x = elbow_x + math.sin(elbow_angle) * forearm_len
        hand_y = elbow_y + math.cos(elbow_angle) * forearm_len

        sleeve_color = CLOTH_SHIRT_ACCENT if is_back else CLOTH_SHIRT
        skin_c = SKIN_SHADOW if is_back else SKIN_TONE

        pygame.draw.line(surface, sleeve_color, (shoulder_x, shoulder_y), (elbow_x, elbow_y), 5)
        pygame.draw.line(surface, skin_c, (elbow_x, elbow_y), (hand_x, hand_y), 4)
        pygame.draw.circle(surface, skin_c, (int(hand_x), int(hand_y)), 3)
