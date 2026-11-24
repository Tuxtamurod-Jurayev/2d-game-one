"""
Humanoid Athletic Runner Entity with Subway Heroes (Jake, Tricky, Fresh, Yutani).
Renders each character accurately according to their iconic visual design:
- Jake: Baseball cap, denim vest, hoodie, blue jeans.
- Tricky: Red beanie, blonde pigtails, glasses, white crop top, baggy jeans.
- Fresh: Tall flat-top fade hair, nerd glasses, green tank top, red shorts, striped tube socks.
- Yutani: Green alien creature onesie with giant cartoon eyes, purple buns, and 4 arms!
Features:
- Balanced, smooth running cadence.
- Double Jump system with 360-degree aerial somersault.
- Low-profile athletic slide pose.
- Dynamic altitude shadow and particle effects.
"""
import math
import random
import pygame
from src.settings import (
    PLAYER_X, GROUND_Y, GRAVITY, JUMP_STRENGTH, DOUBLE_JUMP_STRENGTH,
    CHARACTERS
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
            self.size += 1.5
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
    def __init__(self, character_id="jake"):
        self.character_id = character_id
        self.char_data = self._get_char_data(character_id)
        self.reset()

    def _get_char_data(self, char_id):
        for c in CHARACTERS:
            if c["id"] == char_id:
                return c
        return CHARACTERS[0]

    def set_character(self, char_id):
        self.character_id = char_id
        self.char_data = self._get_char_data(char_id)

    def reset(self):
        self.x = PLAYER_X
        self.y = GROUND_Y
        self.vy = 0
        self.is_grounded = True
        self.is_ducking = False

        # Multi-jump system
        self.jump_count = 0
        self.max_jumps = 2
        self.is_double_jumping = False
        self.flip_angle = 0.0

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
        w = self.current_width
        h = self.current_height
        if self.is_ducking:
            return pygame.Rect(self.x - 24, self.y - h + 2, w - 8, h - 4)
        return pygame.Rect(self.x - 14, self.y - h + 4, w - 4, h - 6)

    def jump(self, sound_mgr):
        if self.is_ducking:
            return

        if self.is_grounded:
            self.vy = JUMP_STRENGTH
            self.is_grounded = False
            self.jump_count = 1
            self.is_double_jumping = False
            sound_mgr.play_jump()

            for _ in range(8):
                self.particles.append(Particle(
                    self.x + random.uniform(-10, 10),
                    self.y - 2,
                    random.uniform(-3, 1),
                    random.uniform(-2, -0.2),
                    (180, 190, 220),
                    random.uniform(4, 6),
                    lifetime=18,
                    decay_rate=0.25
                ))

        elif self.jump_count < self.max_jumps:
            self.vy = DOUBLE_JUMP_STRENGTH
            self.jump_count = 2
            self.is_double_jumping = True
            self.flip_angle = 0.0
            sound_mgr.play_double_jump()

            self.particles.append(Particle(
                self.x, self.y - 8,
                0, 0,
                self.char_data["accent_color"],
                size=8,
                lifetime=20,
                is_ring=True
            ))

            for _ in range(12):
                self.particles.append(Particle(
                    self.x + random.uniform(-6, 6),
                    self.y - 6,
                    random.uniform(-3.5, 3.5),
                    random.uniform(-1, 3.0),
                    random.choice([self.char_data["accent_color"], (255, 255, 255)]),
                    random.uniform(3, 5),
                    lifetime=18,
                    decay_rate=0.22
                ))

    def cut_jump(self):
        if not self.is_grounded and self.vy < -4.5:
            self.vy *= 0.55

    def update(self, keys_pressed, speed_factor=1.0):
        if self.is_grounded:
            if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
                self.is_ducking = True
            else:
                self.is_ducking = False
        else:
            if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
                self.vy += GRAVITY * 1.6

        self.vy += GRAVITY
        self.y += self.vy

        if self.y >= GROUND_Y:
            if not self.is_grounded:
                for _ in range(6):
                    self.particles.append(Particle(
                        self.x + random.uniform(-8, 8),
                        GROUND_Y - 2,
                        random.uniform(-2.5, 2.5),
                        random.uniform(-1.5, -0.2),
                        (190, 200, 230),
                        random.uniform(3, 5),
                        lifetime=14
                    ))
            self.y = GROUND_Y
            self.vy = 0
            self.is_grounded = True
            self.jump_count = 0
            self.is_double_jumping = False
            self.flip_angle = 0.0

        if self.is_double_jumping and not self.is_grounded:
            self.flip_angle += 22.0
            if self.flip_angle >= 360.0:
                self.flip_angle = 0.0
                self.is_double_jumping = False

        # Fluid, balanced animation cadence
        step_rate = 0.26 * (speed_factor / 7.0)
        self.anim_tick += step_rate

        if self.is_grounded:
            if self.is_ducking:
                if random.random() < 0.65:
                    self.particles.append(Particle(
                        self.x - 12 + random.uniform(-5, 5),
                        self.y - 2,
                        random.uniform(-4, -1),
                        random.uniform(-1.5, 0),
                        random.choice([self.char_data["accent_color"], (255, 180, 50), (255, 255, 255)]),
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

        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.is_alive()]

    def draw(self, surface):
        # 1. Ground Shadow (scales with altitude)
        altitude = max(0, GROUND_Y - self.y)
        shadow_scale = max(0.2, 1.0 - (altitude / 260.0))
        shadow_w = int(28 * shadow_scale)
        shadow_h = int(8 * shadow_scale)
        shadow_surf = pygame.Surface((shadow_w * 2, shadow_h * 2), pygame.SRCALPHA)
        shadow_alpha = int(90 * shadow_scale)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, shadow_alpha), (0, 0, shadow_w * 2, shadow_h * 2))
        surface.blit(shadow_surf, (self.x - shadow_w, GROUND_Y - shadow_h // 2))

        # 2. Draw Particles
        for p in self.particles:
            p.draw(surface)

        # 3. Draw Selected Character
        if self.character_id == "jake":
            self._draw_jake(surface)
        elif self.character_id == "tricky":
            self._draw_tricky(surface)
        elif self.character_id == "fresh":
            self._draw_fresh(surface)
        elif self.character_id == "yutani":
            self._draw_yutani(surface)
        else:
            self._draw_jake(surface)

    # ----------------------------------------------------
    # 1. JAKE (Denim vest, hoodie, backwards cap, blue jeans)
    # ----------------------------------------------------
    def _draw_jake(self, surface):
        skin = (244, 202, 172)
        vest = (55, 110, 185)       # Denim blue vest
        hoodie = (230, 230, 235)    # Light grey hoodie underneath
        pants = (38, 55, 95)        # Blue jeans
        shoes = (255, 255, 255)     # White skate sneakers
        shoe_accent = (50, 215, 80) # Green tongue
        cap_white = (255, 255, 255)
        cap_red = (235, 45, 55)

        cycle = self.anim_tick
        bob = math.sin(cycle * 2.0) * 2.5 if (self.is_grounded and not self.is_ducking) else 0
        hip_x, hip_y = self.x, self.y - 28 + bob

        if self.is_ducking:
            # Low slide pose
            slide_y = self.y - 10
            # Torso
            pygame.draw.rect(surface, hoodie, (hip_x - 18, slide_y - 14, 22, 14), border_radius=4)
            pygame.draw.rect(surface, vest, (hip_x - 16, slide_y - 14, 18, 14), border_radius=3)
            # Head with backwards cap
            head_x, head_y = hip_x - 22, slide_y - 14
            pygame.draw.circle(surface, skin, (head_x, head_y), 8)
            pygame.draw.circle(surface, cap_white, (head_x - 1, head_y - 2), 7)
            pygame.draw.rect(surface, cap_red, (head_x - 8, head_y - 5, 8, 4), border_radius=2) # Back visor
            # Slide legs
            pygame.draw.line(surface, pants, (hip_x + 2, slide_y - 4), (hip_x + 28, slide_y - 1), 6)
            pygame.draw.rect(surface, shoes, (hip_x + 24, slide_y - 4, 12, 6), border_radius=2)
            pygame.draw.rect(surface, shoe_accent, (hip_x + 24, slide_y - 4, 4, 6))
            return

        if self.is_double_jumping:
            self._draw_somersault(surface, vest, skin, cap_red)
            return

        leg1_angle = math.sin(cycle) * 0.75 if self.is_grounded else 0.6
        leg2_angle = math.sin(cycle + math.pi) * 0.75 if self.is_grounded else -0.5

        # Back arm & leg
        self._draw_limb(surface, hip_x - 2, hip_y - 14, -leg1_angle * 0.8, 11, 10, hoodie, skin, is_arm=True)
        self._draw_limb(surface, hip_x - 3, hip_y, leg2_angle, 14, 14, pants, shoes, is_arm=False, shoe_accent=shoe_accent)

        # Torso (Hoodie + Denim Vest)
        torso_rect = pygame.Rect(hip_x - 8 + int(4.0 * 0.4), hip_y - 20, 16, 20)
        pygame.draw.rect(surface, hoodie, torso_rect, border_radius=4)
        vest_rect = pygame.Rect(torso_rect.x + 1, torso_rect.y + 2, 14, 18)
        pygame.draw.rect(surface, vest, vest_rect, border_radius=3)
        pygame.draw.line(surface, (255, 255, 255), (vest_rect.centerx, vest_rect.top), (vest_rect.centerx, vest_rect.bottom), 2)

        # Head & Backwards Cap
        head_x, head_y = hip_x + 4, hip_y - 31
        pygame.draw.circle(surface, skin, (head_x, head_y), 9)
        # Cap Dome (White with Red brim facing back)
        pygame.draw.arc(surface, cap_white, (head_x - 8, head_y - 10, 16, 14), 0, math.pi, 8)
        pygame.draw.rect(surface, cap_red, (head_x - 11, head_y - 5, 8, 4), border_radius=2) # Visor facing back
        # Eye & smile
        pygame.draw.rect(surface, (20, 20, 40), (head_x + 4, head_y - 2, 3, 3))
        pygame.draw.arc(surface, (180, 70, 70), (head_x + 2, head_y + 1, 5, 4), math.pi, 2 * math.pi, 2)

        # Front leg & arm
        self._draw_limb(surface, hip_x + 3, hip_y, leg1_angle, 14, 14, pants, shoes, is_arm=False, shoe_accent=shoe_accent)
        self._draw_limb(surface, hip_x + 2, hip_y - 14, -leg2_angle * 0.8, 11, 10, hoodie, skin, is_arm=True)

    # ----------------------------------------------------
    # 2. TRICKY (Red beanie, blonde pigtails, glasses, crop top)
    # ----------------------------------------------------
    def _draw_tricky(self, surface):
        skin = (250, 215, 190)
        beanie = (235, 40, 50)      # Red beanie hat
        blonde = (252, 222, 98)     # Blonde pigtails
        crop_top = (255, 255, 255)  # White crop top
        jeans = (70, 130, 200)      # Baggy skater jeans
        belt = (30, 30, 35)
        shoes = (255, 255, 255)
        shoe_accent = (235, 40, 50)

        cycle = self.anim_tick
        bob = math.sin(cycle * 2.0) * 2.5 if (self.is_grounded and not self.is_ducking) else 0
        hip_x, hip_y = self.x, self.y - 28 + bob

        if self.is_ducking:
            slide_y = self.y - 10
            pygame.draw.rect(surface, crop_top, (hip_x - 18, slide_y - 14, 18, 12), border_radius=4)
            # Head with beanie
            head_x, head_y = hip_x - 22, slide_y - 14
            pygame.draw.circle(surface, skin, (head_x, head_y), 8)
            pygame.draw.circle(surface, beanie, (head_x - 1, head_y - 3), 8)
            # Blonde pigtail streaming back
            pygame.draw.ellipse(surface, blonde, (head_x - 12, head_y - 2, 10, 6))
            pygame.draw.line(surface, jeans, (hip_x + 2, slide_y - 4), (hip_x + 28, slide_y - 1), 7)
            pygame.draw.rect(surface, shoes, (hip_x + 24, slide_y - 4, 12, 6), border_radius=2)
            return

        if self.is_double_jumping:
            self._draw_somersault(surface, crop_top, skin, beanie)
            return

        leg1_angle = math.sin(cycle) * 0.75 if self.is_grounded else 0.6
        leg2_angle = math.sin(cycle + math.pi) * 0.75 if self.is_grounded else -0.5

        # Back arm & leg (baggy jeans)
        self._draw_limb(surface, hip_x - 2, hip_y - 14, -leg1_angle * 0.8, 10, 9, skin, skin, is_arm=True)
        self._draw_limb(surface, hip_x - 3, hip_y, leg2_angle, 14, 14, jeans, shoes, is_arm=False, shoe_accent=shoe_accent, is_baggy=True)

        # Torso (Crop Top + Midriff + Belt)
        torso_rect = pygame.Rect(hip_x - 7, hip_y - 19, 14, 10)
        pygame.draw.rect(surface, crop_top, torso_rect, border_radius=3)
        # Exposed midriff
        pygame.draw.rect(surface, skin, (hip_x - 6, hip_y - 9, 12, 5))
        # Belt
        pygame.draw.rect(surface, belt, (hip_x - 7, hip_y - 4, 14, 3))

        # Head & Red Beanie + Blonde Pigtails
        head_x, head_y = hip_x + 3, hip_y - 30
        pygame.draw.circle(surface, skin, (head_x, head_y), 9)

        # Blonde pigtails (front and back puff)
        flutter = math.sin(cycle * 3.0) * 3
        pygame.draw.ellipse(surface, blonde, (head_x - 12 + int(flutter), head_y - 4, 9, 12))
        pygame.draw.ellipse(surface, blonde, (head_x + 4, head_y + 1, 8, 9))

        # Red slouchy beanie covering top of head
        pygame.draw.ellipse(surface, beanie, (head_x - 8, head_y - 12, 16, 12))
        pygame.draw.rect(surface, (210, 30, 40), (head_x - 8, head_y - 6, 16, 4), border_radius=2)

        # Nerd glasses (black thick frames)
        pygame.draw.rect(surface, (15, 15, 20), (head_x + 1, head_y - 3, 8, 6), 2, border_radius=2)
        pygame.draw.rect(surface, (20, 20, 40), (head_x + 4, head_y - 2, 3, 3))

        # Front leg & arm
        self._draw_limb(surface, hip_x + 3, hip_y, leg1_angle, 14, 14, jeans, shoes, is_arm=False, shoe_accent=shoe_accent, is_baggy=True)
        self._draw_limb(surface, hip_x + 2, hip_y - 14, -leg2_angle * 0.8, 10, 9, skin, skin, is_arm=True)

    # ----------------------------------------------------
    # 3. FRESH (Tall flat-top fade, glasses, tank top, shorts, tube socks)
    # ----------------------------------------------------
    def _draw_fresh(self, surface):
        skin = (165, 105, 65)
        hair = (22, 16, 16)         # High flat-top fade
        tank_top = (45, 215, 75)    # Green tank top
        shorts = (235, 45, 55)      # Red athletic shorts
        socks = (250, 250, 250)     # White tube socks
        shoes = (160, 65, 45)       # High-top kicks

        cycle = self.anim_tick
        bob = math.sin(cycle * 2.0) * 2.5 if (self.is_grounded and not self.is_ducking) else 0
        hip_x, hip_y = self.x, self.y - 28 + bob

        if self.is_ducking:
            slide_y = self.y - 10
            pygame.draw.rect(surface, tank_top, (hip_x - 18, slide_y - 14, 20, 14), border_radius=4)
            head_x, head_y = hip_x - 22, slide_y - 14
            pygame.draw.circle(surface, skin, (head_x, head_y), 8)
            # Tall flat-top haircut horizontally
            pygame.draw.rect(surface, hair, (head_x - 14, head_y - 6, 10, 12), border_radius=2)
            pygame.draw.line(surface, shorts, (hip_x + 2, slide_y - 4), (hip_x + 16, slide_y - 2), 6)
            pygame.draw.line(surface, skin, (hip_x + 16, slide_y - 2), (hip_x + 26, slide_y - 1), 5)
            pygame.draw.rect(surface, shoes, (hip_x + 24, slide_y - 4, 12, 6), border_radius=2)
            return

        if self.is_double_jumping:
            self._draw_somersault(surface, tank_top, skin, hair)
            return

        leg1_angle = math.sin(cycle) * 0.75 if self.is_grounded else 0.6
        leg2_angle = math.sin(cycle + math.pi) * 0.75 if self.is_grounded else -0.5

        # Back arm & leg (shorts + tube socks + shoes)
        self._draw_fresh_arm(surface, hip_x - 2, hip_y - 14, -leg1_angle * 0.8, skin)
        self._draw_fresh_leg(surface, hip_x - 3, hip_y, leg2_angle, shorts, skin, socks, shoes, is_back=True)

        # Torso (Green Tank Top)
        torso_rect = pygame.Rect(hip_x - 7, hip_y - 19, 14, 18)
        pygame.draw.rect(surface, tank_top, torso_rect, border_radius=4)
        # Collar line
        pygame.draw.arc(surface, (30, 170, 55), (torso_rect.centerx - 4, torso_rect.top, 8, 6), 0, math.pi, 2)

        # Head & Tall High-Top Fade
        head_x, head_y = hip_x + 4, hip_y - 30
        pygame.draw.circle(surface, skin, (head_x, head_y), 9)

        # Iconic Tall Flat-Top Haircut!
        hair_rect = pygame.Rect(head_x - 7, head_y - 23, 14, 16)
        pygame.draw.rect(surface, hair, hair_rect, border_radius=2)
        # Fade sides
        pygame.draw.rect(surface, (50, 35, 30), (head_x - 7, head_y - 12, 4, 6))

        # Nerd Glasses (Rectangular black frames)
        pygame.draw.rect(surface, (15, 15, 20), (head_x + 1, head_y - 4, 8, 6), 2, border_radius=1)
        pygame.draw.rect(surface, (255, 255, 255), (head_x + 3, head_y - 3, 4, 3))
        pygame.draw.rect(surface, (20, 20, 40), (head_x + 5, head_y - 3, 2, 3))

        # Front leg & arm
        self._draw_fresh_leg(surface, hip_x + 3, hip_y, leg1_angle, shorts, skin, socks, shoes, is_back=False)
        self._draw_fresh_arm(surface, hip_x + 2, hip_y - 14, -leg2_angle * 0.8, skin)

    def _draw_fresh_leg(self, surface, hip_x, hip_y, angle, shorts, skin, socks, shoes, is_back=False):
        thigh_len, shin_len = 14, 14
        knee_bend = math.sin(angle) * 0.4 if angle > 0 else -math.sin(angle) * 0.8
        kx = hip_x + math.sin(angle) * thigh_len
        ky = hip_y + math.cos(angle) * thigh_len
        fx = kx + math.sin(angle - knee_bend * 0.5) * shin_len
        fy = min(ky + math.cos(angle - knee_bend * 0.5) * shin_len, GROUND_Y)

        # Thigh with shorts
        pygame.draw.line(surface, shorts, (hip_x, hip_y), (hip_x + math.sin(angle) * 9, hip_y + math.cos(angle) * 9), 6)
        pygame.draw.line(surface, skin, (hip_x + math.sin(angle) * 9, hip_y + math.cos(angle) * 9), (kx, ky), 5)

        # Calf with tall tube sock
        mid_calf_x = kx + (fx - kx) * 0.4
        mid_calf_y = ky + (fy - ky) * 0.4
        pygame.draw.line(surface, skin, (kx, ky), (mid_calf_x, mid_calf_y), 5)
        # Tube sock (white with red/green stripes)
        pygame.draw.line(surface, socks, (mid_calf_x, mid_calf_y), (fx, fy), 5)
        stripe_x = kx + (fx - kx) * 0.55
        stripe_y = ky + (fy - ky) * 0.55
        pygame.draw.circle(surface, (220, 40, 50), (int(stripe_x), int(stripe_y)), 2)

        # High-top kicks
        pygame.draw.rect(surface, shoes, (fx - 3, fy - 6, 11, 6), border_radius=2)
        pygame.draw.rect(surface, (255, 255, 255), (fx - 3, fy - 2, 11, 2))

    def _draw_fresh_arm(self, surface, shoulder_x, shoulder_y, angle, skin):
        arm_len, forearm_len = 11, 10
        elbow_angle = angle + 0.35
        ex = shoulder_x + math.sin(angle) * arm_len
        ey = shoulder_y + math.cos(angle) * arm_len
        hx = ex + math.sin(elbow_angle) * forearm_len
        hy = ey + math.cos(elbow_angle) * forearm_len
        pygame.draw.line(surface, skin, (shoulder_x, shoulder_y), (ex, ey), 4)
        pygame.draw.line(surface, skin, (ex, ey), (hx, hy), 4)
        pygame.draw.circle(surface, skin, (int(hx), int(hy)), 3)

    # ----------------------------------------------------
    # 4. YUTANI (Green alien onesie, giant eyes, purple buns, 4 arms)
    # ----------------------------------------------------
    def _draw_yutani(self, surface):
        skin = (245, 205, 180)
        alien_green = (125, 215, 55) # Bright green monster suit
        dark_green = (95, 180, 35)
        purple = (185, 60, 250)      # Purple streaks & shoes
        eyes_white = (255, 255, 255)
        pupil = (25, 25, 30)

        cycle = self.anim_tick
        bob = math.sin(cycle * 2.0) * 2.5 if (self.is_grounded and not self.is_ducking) else 0
        hip_x, hip_y = self.x, self.y - 28 + bob

        if self.is_ducking:
            slide_y = self.y - 10
            # Alien onesie slide
            pygame.draw.rect(surface, alien_green, (hip_x - 18, slide_y - 14, 22, 14), border_radius=6)
            head_x, head_y = hip_x - 22, slide_y - 14
            pygame.draw.circle(surface, alien_green, (head_x, head_y), 11)
            # Giant alien eyes on hood
            pygame.draw.circle(surface, eyes_white, (head_x - 4, head_y - 10), 5)
            pygame.draw.circle(surface, pupil, (head_x - 4, head_y - 10), 3)
            pygame.draw.line(surface, alien_green, (hip_x + 2, slide_y - 4), (hip_x + 28, slide_y - 1), 7)
            pygame.draw.rect(surface, purple, (hip_x + 24, slide_y - 4, 12, 6), border_radius=2)
            return

        if self.is_double_jumping:
            self._draw_somersault(surface, alien_green, skin, alien_green)
            return

        leg1_angle = math.sin(cycle) * 0.75 if self.is_grounded else 0.6
        leg2_angle = math.sin(cycle + math.pi) * 0.75 if self.is_grounded else -0.5

        # Back arm 1 and Back arm 2 (4 ARMS on suit!)
        self._draw_limb(surface, hip_x - 2, hip_y - 16, -leg1_angle * 0.8, 10, 9, alien_green, alien_green, is_arm=True)
        self._draw_limb(surface, hip_x - 4, hip_y - 10, -leg1_angle * 0.6 - 0.4, 8, 7, dark_green, dark_green, is_arm=True) # Extra suit arm!

        # Back leg
        self._draw_limb(surface, hip_x - 3, hip_y, leg2_angle, 14, 14, alien_green, purple, is_arm=False)

        # Torso (Green Alien Onesie Jumpsuit with tummy patch)
        torso_rect = pygame.Rect(hip_x - 8, hip_y - 20, 16, 20)
        pygame.draw.rect(surface, alien_green, torso_rect, border_radius=6)
        # Belly patch
        pygame.draw.ellipse(surface, (160, 235, 95), (torso_rect.centerx - 5, torso_rect.y + 4, 10, 14))

        # Head inside Alien Hood + Giant Eyes + Purple hair buns
        head_x, head_y = hip_x + 3, hip_y - 30

        # Hair buns sticking out with purple streak
        pygame.draw.circle(surface, (30, 25, 35), (head_x - 9, head_y - 4), 5)
        pygame.draw.circle(surface, purple, (head_x - 9, head_y - 6), 3)

        # Green Alien Hood
        pygame.draw.circle(surface, alien_green, (head_x, head_y), 11)

        # Face opening
        pygame.draw.circle(surface, skin, (head_x + 2, head_y + 1), 7)
        # Face eyes & smile
        pygame.draw.rect(surface, (20, 20, 35), (head_x + 4, head_y, 3, 3))
        pygame.draw.arc(surface, (190, 70, 70), (head_x + 2, head_y + 3, 4, 3), math.pi, 2 * math.pi, 1)

        # Giant Cartoon Alien Eyes on top of Hood!
        eye1_x, eye1_y = head_x - 5, head_y - 11
        eye2_x, eye2_y = head_x + 4, head_y - 11
        pygame.draw.circle(surface, eyes_white, (eye1_x, eye1_y), 6)
        pygame.draw.circle(surface, eyes_white, (eye2_x, eye2_y), 6)
        pygame.draw.circle(surface, pupil, (eye1_x, eye1_y), 3)
        pygame.draw.circle(surface, pupil, (eye2_x, eye2_y), 3)
        # Antennae stalks
        pygame.draw.line(surface, dark_green, (eye1_x - 2, eye1_y - 5), (eye1_x - 4, eye1_y - 9), 2)
        pygame.draw.line(surface, dark_green, (eye2_x + 2, eye2_y - 5), (eye2_x + 4, eye2_y - 9), 2)

        # Front leg
        self._draw_limb(surface, hip_x + 3, hip_y, leg1_angle, 14, 14, alien_green, purple, is_arm=False)

        # Front arm 1 and Front arm 2 (4 arms total!)
        self._draw_limb(surface, hip_x + 2, hip_y - 16, -leg2_angle * 0.8, 10, 9, alien_green, alien_green, is_arm=True)
        self._draw_limb(surface, hip_x + 4, hip_y - 10, -leg2_angle * 0.6 + 0.4, 8, 7, dark_green, dark_green, is_arm=True)

    # ----------------------------------------------------
    # General Limb & Flip Utilities
    # ----------------------------------------------------
    def _draw_limb(self, surface, hip_x, hip_y, angle, upper_len, lower_len, upper_col, lower_col, is_arm=False, shoe_accent=None, is_baggy=False):
        if is_arm:
            elbow_angle = angle + 0.35
            ex = hip_x + math.sin(angle) * upper_len
            ey = hip_y + math.cos(angle) * upper_len
            hx = ex + math.sin(elbow_angle) * lower_len
            hy = ey + math.cos(elbow_angle) * lower_len
            pygame.draw.line(surface, upper_col, (hip_x, hip_y), (ex, ey), 5)
            pygame.draw.line(surface, lower_col, (ex, ey), (hx, hy), 4)
            pygame.draw.circle(surface, lower_col, (int(hx), int(hy)), 3)
        else:
            knee_bend = math.sin(angle) * 0.4 if angle > 0 else -math.sin(angle) * 0.8
            kx = hip_x + math.sin(angle) * upper_len
            ky = hip_y + math.cos(angle) * upper_len
            fx = kx + math.sin(angle - knee_bend * 0.5) * lower_len
            fy = min(ky + math.cos(angle - knee_bend * 0.5) * lower_len, GROUND_Y)

            thickness = 7 if is_baggy else 6
            pygame.draw.line(surface, upper_col, (hip_x, hip_y), (kx, ky), thickness)
            pygame.draw.line(surface, upper_col, (kx, ky), (fx, fy), thickness - 1)

            # Sneaker
            shoe_w = 11
            pygame.draw.rect(surface, lower_col, (fx - 3, fy - 6, shoe_w, 6), border_radius=2)
            if shoe_accent:
                pygame.draw.rect(surface, shoe_accent, (fx + 2, fy - 6, 3, 6))
            pygame.draw.rect(surface, (255, 255, 255), (fx - 3, fy - 2, shoe_w, 2))

    def _draw_somersault(self, surface, torso_col, skin_col, head_col):
        temp_w, temp_h = 70, 70
        temp_surf = pygame.Surface((temp_w, temp_h), pygame.SRCALPHA)
        cx, cy = temp_w // 2, temp_h // 2

        pygame.draw.rect(temp_surf, torso_col, (cx - 8, cy - 10, 16, 18), border_radius=4)
        pygame.draw.circle(temp_surf, skin_col, (cx + 4, cy - 18), 8)
        pygame.draw.circle(temp_surf, head_col, (cx + 4, cy - 22), 6)
        pygame.draw.line(temp_surf, (40, 50, 75), (cx - 4, cy + 4), (cx + 8, cy + 14), 6)
        pygame.draw.line(temp_surf, (40, 50, 75), (cx + 8, cy + 14), (cx - 2, cy + 18), 5)
        pygame.draw.rect(temp_surf, (255, 255, 255), (cx - 4, cy + 16, 9, 5), border_radius=2)

        rotated = pygame.transform.rotate(temp_surf, -self.flip_angle)
        new_rect = rotated.get_rect(center=(self.x, self.y - 28))
        surface.blit(rotated, new_rect.topleft)
