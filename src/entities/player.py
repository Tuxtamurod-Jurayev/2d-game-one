"""
Humanoid Athletic Runner Entity.
Features anatomically accurate human proportions:
- Distinct Head, Hair (with wind dynamics), Face/Eye.
- Athletic Torso/Jacket with runner lean.
- Dual-jointed Arms swinging naturally in opposition to legs.
- Dual-jointed Running Legs with knee flexion and stylish sneakers.
- Distinct Jump pose (arms balance, legs tuck) and low-profile Slide pose.
- Particle generation: footstep dust, jump poof, slide friction sparks.
"""
import math
import random
import pygame
from src.settings import (
    PLAYER_X, GROUND_Y, GRAVITY, JUMP_STRENGTH,
    SKIN_TONE, SKIN_SHADOW, HAIR_COLOR, HAIR_HIGHLIGHT,
    CLOTH_SHIRT, CLOTH_SHIRT_ACCENT, CLOTH_PANTS,
    CLOTH_SHOES, CLOTH_SHOES_SOLES
)

class Particle:
    def __init__(self, x, y, vx, vy, color, size, lifetime, decay_rate=0.1):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.decay_rate = decay_rate
        self.age = 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.age += 1
        self.size = max(0, self.size - self.decay_rate)

    def is_alive(self):
        return self.age < self.lifetime and self.size > 0

    def draw(self, surface):
        if self.size > 0:
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

        # Hitbox sizes
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
        # Precise, fair hitbox aligned to the human body
        w = self.current_width
        h = self.current_height
        if self.is_ducking:
            return pygame.Rect(self.x - 24, self.y - h + 2, w - 8, h - 4)
        return pygame.Rect(self.x - 14, self.y - h + 4, w - 4, h - 6)

    def jump(self, sound_mgr):
        if self.is_grounded and not self.is_ducking:
            self.vy = JUMP_STRENGTH
            self.is_grounded = False
            sound_mgr.play_jump()

            # Jump liftoff dust burst
            for _ in range(10):
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

    def update(self, keys_pressed, speed_factor=1.0):
        # 1. Slide / Duck control
        if self.is_grounded:
            if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
                self.is_ducking = True
            else:
                self.is_ducking = False
        else:
            # Quick-dive if holding DOWN while airborne
            if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
                self.vy += GRAVITY * 1.6

        # 2. Gravity & Physics
        self.vy += GRAVITY
        self.y += self.vy

        if self.y >= GROUND_Y:
            if not self.is_grounded:
                # Landing footstep dust poof
                for _ in range(6):
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

        # 3. Animation cycle
        step_rate = 0.28 * (speed_factor / 7.0)
        self.anim_tick += step_rate

        # 4. Particles (Running foot dust or slide sparks)
        if self.is_grounded:
            if self.is_ducking:
                # Slide friction spark & smoke
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
                # Footstep puff when leg strikes down
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
        # 1. Draw particles (behind character)
        for p in self.particles:
            p.draw(surface)

        if self.is_ducking:
            self._draw_sliding_human(surface)
        elif not self.is_grounded:
            self._draw_jumping_human(surface)
        else:
            self._draw_running_human(surface)

    def _draw_running_human(self, surface):
        """Draws human runner with realistic multi-joint limbs and torso lean."""
        cycle = self.anim_tick
        bob = math.sin(cycle * 2.0) * 2.5  # Vertical torso bounce
        lean = 4.0                        # Forward torso tilt

        # Base hip joint position
        hip_x = self.x
        hip_y = self.y - 28 + bob

        # Calculate Leg phase angles (opposite phases)
        leg1_angle = math.sin(cycle) * 0.75
        leg2_angle = math.sin(cycle + math.pi) * 0.75

        # --- A. BACK ARM (Drawn behind body) ---
        arm_back_angle = -leg1_angle * 0.8
        self._draw_human_arm(surface, hip_x - 2, hip_y - 14, arm_back_angle, is_back=True)

        # --- B. BACK LEG (Drawn behind body) ---
        self._draw_human_leg(surface, hip_x - 3, hip_y, leg2_angle, is_back=True)

        # --- C. TORSO & JACKET ---
        # Athletic torso with forward lean
        torso_w, torso_h = 16, 20
        torso_rect = pygame.Rect(hip_x - 8 + int(lean * 0.4), hip_y - torso_h, torso_w, torso_h)
        pygame.draw.rect(surface, CLOTH_SHIRT, torso_rect, border_radius=4)
        # Jacket center zipper & collar detail
        pygame.draw.line(surface, CLOTH_SHIRT_ACCENT, (torso_rect.centerx, torso_rect.top + 3), (torso_rect.centerx - 1, torso_rect.bottom - 2), 2)
        pygame.draw.line(surface, (0, 240, 255), (torso_rect.left + 2, torso_rect.top + 4), (torso_rect.left + 2, torso_rect.bottom - 4), 2)

        # --- D. HEAD, FACE & HAIR ---
        head_x = hip_x + int(lean)
        head_y = hip_y - torso_h - 11
        # Neck
        pygame.draw.rect(surface, SKIN_SHADOW, (head_x - 3, head_y + 9, 6, 4))
        # Face / Head
        pygame.draw.circle(surface, SKIN_TONE, (head_x, head_y), 9)
        # Eye looking forward
        pygame.draw.rect(surface, (255, 255, 255), (head_x + 3, head_y - 2, 4, 3))
        pygame.draw.rect(surface, (20, 20, 40), (head_x + 5, head_y - 2, 2, 3))
        # Eyebrow
        pygame.draw.line(surface, HAIR_COLOR, (head_x + 2, head_y - 4), (head_x + 7, head_y - 4), 2)
        # Stylish wind-blown hair
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
        """Draws dynamic athletic mid-air jump silhouette."""
        hip_x = self.x
        hip_y = self.y - 26

        # --- BACK ARM & LEG ---
        # Arms raised up & back for aerial balance
        self._draw_human_arm(surface, hip_x - 4, hip_y - 14, angle=-1.1, is_back=True)
        # Back leg trailing
        self._draw_human_leg(surface, hip_x - 4, hip_y, angle=-0.5, is_back=True, bend_knee=0.8)

        # --- TORSO ---
        torso_rect = pygame.Rect(hip_x - 8, hip_y - 20, 16, 20)
        pygame.draw.rect(surface, CLOTH_SHIRT, torso_rect, border_radius=4)
        pygame.draw.line(surface, (0, 240, 255), (torso_rect.left + 2, torso_rect.top + 3), (torso_rect.left + 2, torso_rect.bottom - 3), 2)

        # --- HEAD & HAIR (Wind blowing hair upward/backward) ---
        head_x = hip_x + 2
        head_y = hip_y - 31
        pygame.draw.rect(surface, SKIN_SHADOW, (head_x - 3, head_y + 9, 6, 4))
        pygame.draw.circle(surface, SKIN_TONE, (head_x, head_y), 9)
        # Eye
        pygame.draw.rect(surface, (255, 255, 255), (head_x + 3, head_y - 2, 4, 3))
        pygame.draw.rect(surface, (20, 20, 40), (head_x + 5, head_y - 2, 2, 3))
        # Hair swept back by vertical draft
        hair_points = [
            (head_x - 8, head_y + 2),
            (head_x - 12, head_y - 12),
            (head_x + 5, head_y - 11),
            (head_x + 8, head_y - 5),
            (head_x - 3, head_y - 3)
        ]
        pygame.draw.polygon(surface, HAIR_COLOR, hair_points)

        # --- FRONT LEG (Tucked forward) ---
        self._draw_human_leg(surface, hip_x + 3, hip_y, angle=0.6, is_back=False, bend_knee=1.2)

        # --- FRONT ARM ---
        self._draw_human_arm(surface, hip_x + 3, hip_y - 14, angle=1.0, is_back=False)

    def _draw_sliding_human(self, surface):
        """Draws human in a low slide posture."""
        slide_y = self.y - 10
        slide_x = self.x

        # Torso leaning back close to ground
        torso_rect = pygame.Rect(slide_x - 18, slide_y - 14, 22, 14)
        pygame.draw.rect(surface, CLOTH_SHIRT, torso_rect, border_radius=4)

        # Head tilted forward
        head_x = slide_x - 22
        head_y = slide_y - 14
        pygame.draw.circle(surface, SKIN_TONE, (head_x, head_y), 8)
        # Eye
        pygame.draw.rect(surface, (255, 255, 255), (head_x + 2, head_y - 1, 3, 2))
        pygame.draw.rect(surface, (20, 20, 40), (head_x + 3, head_y - 1, 2, 2))
        # Hair blown backward
        pygame.draw.polygon(surface, HAIR_COLOR, [
            (head_x - 7, head_y + 1),
            (head_x - 14, head_y - 7),
            (head_x + 2, head_y - 8),
            (head_x + 6, head_y - 3)
        ])

        # Extended Front Leg (sliding on the ground)
        front_leg_points = [
            (slide_x + 2, slide_y - 4),
            (slide_x + 22, slide_y - 2),
            (slide_x + 30, slide_y - 1)
        ]
        pygame.draw.lines(surface, CLOTH_PANTS, False, front_leg_points, 6)
        # Sneaker on extended foot
        pygame.draw.rect(surface, CLOTH_SHOES, (slide_x + 24, slide_y - 4, 12, 6), border_radius=2)
        pygame.draw.rect(surface, CLOTH_SHOES_SOLES, (slide_x + 24, slide_y + 1, 12, 2))

        # Bent Back Leg (tucked under)
        pygame.draw.line(surface, (20, 25, 40), (slide_x - 8, slide_y - 4), (slide_x + 6, slide_y + 1), 6)

        # Support Arm on ground
        pygame.draw.line(surface, SKIN_TONE, (slide_x - 6, slide_y - 8), (slide_x - 2, slide_y + 2), 4)

    def _draw_human_leg(self, surface, hip_x, hip_y, angle, is_back=False, bend_knee=None):
        """Calculates thigh, knee bend, and sneaker placement."""
        thigh_len = 14
        shin_len = 14

        # Compute knee flexion
        if bend_knee is None:
            # Automatic dynamic knee bend based on stride phase
            knee_bend = math.sin(angle) * 0.4 if angle > 0 else -math.sin(angle) * 0.8
        else:
            knee_bend = bend_knee

        knee_angle = angle + knee_bend
        knee_x = hip_x + math.sin(angle) * thigh_len
        knee_y = hip_y + math.cos(angle) * thigh_len

        foot_angle = angle - knee_bend * 0.5
        foot_x = knee_x + math.sin(foot_angle) * shin_len
        foot_y = knee_y + math.cos(foot_angle) * shin_len

        # Clamp foot above ground plane
        foot_y = min(foot_y, GROUND_Y)

        pants_color = (25, 28, 42) if is_back else CLOTH_PANTS
        shoe_color = (200, 50, 75) if is_back else CLOTH_SHOES

        # Thigh & Shin
        pygame.draw.line(surface, pants_color, (hip_x, hip_y), (knee_x, knee_y), 6)
        pygame.draw.line(surface, pants_color, (knee_x, knee_y), (foot_x, foot_y), 5)

        # Sneaker with white sole
        shoe_w, shoe_h = 10, 6
        pygame.draw.rect(surface, shoe_color, (foot_x - 3, foot_y - shoe_h, shoe_w, shoe_h), border_radius=2)
        pygame.draw.rect(surface, CLOTH_SHOES_SOLES, (foot_x - 3, foot_y - 2, shoe_w, 2))

    def _draw_human_arm(self, surface, shoulder_x, shoulder_y, angle, is_back=False):
        """Calculates upper arm, elbow, forearm and hand."""
        arm_len = 11
        forearm_len = 10

        elbow_angle = angle + 0.35
        elbow_x = shoulder_x + math.sin(angle) * arm_len
        elbow_y = shoulder_y + math.cos(angle) * arm_len

        hand_x = elbow_x + math.sin(elbow_angle) * forearm_len
        hand_y = elbow_y + math.cos(elbow_angle) * forearm_len

        sleeve_color = CLOTH_SHIRT_ACCENT if is_back else CLOTH_SHIRT
        skin_c = SKIN_SHADOW if is_back else SKIN_TONE

        # Upper arm sleeve
        pygame.draw.line(surface, sleeve_color, (shoulder_x, shoulder_y), (elbow_x, elbow_y), 5)
        # Forearm / Hand
        pygame.draw.line(surface, skin_c, (elbow_x, elbow_y), (hand_x, hand_y), 4)
        # Fist
        pygame.draw.circle(surface, skin_c, (int(hand_x), int(hand_y)), 3)
