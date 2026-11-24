"""
Modern Minimalist Stage-Reactive HUD with Character Badge and Vector Icons.
Dynamically adapts color schemes, glowing borders, and stage banners!
"""
import math
import pygame
from src.settings import (
    SCREEN_WIDTH, COLOR_TEXT_MAIN, COLOR_TEXT_GOLD, STAGES
)
from src.ui.icons import (
    draw_trophy, draw_coin_icon, draw_speed_icon, draw_runner_icon
)

class HUD:
    def __init__(self):
        pygame.font.init()
        self.font_main = pygame.font.SysFont("Consolas", 20, bold=True)
        self.font_small = pygame.font.SysFont("Consolas", 15, bold=True)
        self.font_stage = pygame.font.SysFont("Consolas", 13, bold=True)
        self.font_char = pygame.font.SysFont("Consolas", 12, bold=True)
        self.font_banner_title = pygame.font.SysFont("Consolas", 26, bold=True)
        self.font_banner_sub = pygame.font.SysFont("Consolas", 15, bold=True)
        self.tick = 0

    def draw_glass_pill(self, surface, rect, border_color=(0, 240, 255, 110), bg_color=(18, 14, 34, 185)):
        badge = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(badge, bg_color, (0, 0, rect.width, rect.height), border_radius=rect.height // 2)
        pygame.draw.rect(badge, border_color, (0, 0, rect.width, rect.height), width=1, border_radius=rect.height // 2)
        pygame.draw.line(badge, (255, 255, 255, 45), (rect.height // 2, 1), (rect.width - rect.height // 2, 1), 1)
        surface.blit(badge, (rect.x, rect.y))

    def draw(self, surface, score_mgr, speed, stage=None, stage_progress=0.0, banner_timer=0, char_data=None):
        self.tick += 1
        if stage is None:
            stage = STAGES[0]

        accent = stage["accent"]
        secondary = stage["secondary"]
        char_accent = char_data["accent_color"] if char_data else secondary

        # ----------------------------------------------------
        # 1. SCORE BADGE (Top Left)
        # ----------------------------------------------------
        score_val = f"{int(score_mgr.current_score):06d}"
        score_rect = pygame.Rect(20, 18, 150, 36)
        border_col = (secondary[0], secondary[1], secondary[2], 120)
        self.draw_glass_pill(surface, score_rect, border_color=border_col)
        draw_runner_icon(surface, score_rect.x + 20, score_rect.centery, size=18, color=char_accent)
        score_txt = self.font_main.render(score_val, True, COLOR_TEXT_MAIN)
        surface.blit(score_txt, (score_rect.x + 36, score_rect.centery - score_txt.get_height() // 2))

        # ----------------------------------------------------
        # 2. RUNNER HERO BADGE (Top Left-Center)
        # ----------------------------------------------------
        if char_data:
            hero_rect = pygame.Rect(180, 18, 105, 36)
            hero_border = (char_accent[0], char_accent[1], char_accent[2], 130)
            self.draw_glass_pill(surface, hero_rect, border_color=hero_border)
            hero_txt = self.font_char.render(char_data["name"], True, char_accent)
            surface.blit(hero_txt, (hero_rect.centerx - hero_txt.get_width() // 2, hero_rect.centery - hero_txt.get_height() // 2))

        # ----------------------------------------------------
        # 3. STAGE BADGE & PROGRESS BAR (Top Left-Center 2)
        # ----------------------------------------------------
        stage_x = 295 if char_data else 180
        stage_rect = pygame.Rect(stage_x, 18, 150, 36)
        stage_border = (accent[0], accent[1], accent[2], 130)
        self.draw_glass_pill(surface, stage_rect, border_color=stage_border)

        stage_label = f"STAGE {stage['id']}"
        stg_txt = self.font_stage.render(stage_label, True, accent)
        surface.blit(stg_txt, (stage_rect.x + 12, stage_rect.y + 4))

        # Stage Progress Bar
        bar_x = stage_rect.x + 12
        bar_y = stage_rect.y + 22
        bar_w = 126
        bar_h = 7
        pygame.draw.rect(surface, (30, 25, 50), (bar_x, bar_y, bar_w, bar_h), border_radius=3)
        fill_w = max(4, int(bar_w * min(1.0, max(0.0, stage_progress))))
        pygame.draw.rect(surface, accent, (bar_x, bar_y, fill_w, bar_h), border_radius=3)

        # ----------------------------------------------------
        # 4. COINS BADGE (Top Center-Right)
        # ----------------------------------------------------
        coins_rect = pygame.Rect(SCREEN_WIDTH // 2 + 10, 18, 115, 36)
        self.draw_glass_pill(surface, coins_rect, border_color=(255, 215, 0, 110))
        draw_coin_icon(surface, coins_rect.x + 22, coins_rect.centery, size=20, anim_tick=self.tick)
        coins_txt = self.font_main.render(f"x {score_mgr.coins}", True, COLOR_TEXT_GOLD)
        surface.blit(coins_txt, (coins_rect.x + 42, coins_rect.centery - coins_txt.get_height() // 2))

        # ----------------------------------------------------
        # 5. HIGH-SCORE BADGE (Top Right - Left of Speed)
        # ----------------------------------------------------
        hi_val = f"{int(score_mgr.high_score):06d}"
        hi_rect = pygame.Rect(SCREEN_WIDTH - 265, 18, 140, 36)
        self.draw_glass_pill(surface, hi_rect, border_color=(255, 180, 50, 110))
        draw_trophy(surface, hi_rect.x + 20, hi_rect.centery, size=18, color=COLOR_TEXT_GOLD)
        hi_txt = self.font_small.render(hi_val, True, COLOR_TEXT_GOLD)
        surface.blit(hi_txt, (hi_rect.x + 38, hi_rect.centery - hi_txt.get_height() // 2))

        # ----------------------------------------------------
        # 6. SPEED METER BADGE (Top Right)
        # ----------------------------------------------------
        speed_rect = pygame.Rect(SCREEN_WIDTH - 115, 18, 95, 36)
        speed_border = (accent[0], accent[1], accent[2], 120)
        self.draw_glass_pill(surface, speed_rect, border_color=speed_border)
        draw_speed_icon(surface, speed_rect.x + 18, speed_rect.centery, size=18, color=accent)
        speed_txt = self.font_small.render(f"{speed:.1f}x", True, accent)
        surface.blit(speed_txt, (speed_rect.x + 34, speed_rect.centery - speed_txt.get_height() // 2))

        # ----------------------------------------------------
        # 7. STAGE LEVEL-UP BANNER
        # ----------------------------------------------------
        if banner_timer > 0:
            alpha = min(255, int(banner_timer * 4.5))
            bw, bh = 460, 68
            bx = (SCREEN_WIDTH - bw) // 2
            by = 85

            banner_surf = pygame.Surface((bw, bh), pygame.SRCALPHA)
            pygame.draw.rect(banner_surf, (16, 12, 32, min(230, alpha)), (0, 0, bw, bh), border_radius=14)
            pygame.draw.rect(banner_surf, (accent[0], accent[1], accent[2], min(255, alpha)), (0, 0, bw, bh), width=2, border_radius=14)
            surface.blit(banner_surf, (bx, by))

            title_str = f"★ STAGE {stage['id']}: {stage['name']} ★"
            t_surf = self.font_banner_title.render(title_str, True, accent)
            surface.blit(t_surf, (bx + (bw - t_surf.get_width()) // 2, by + 10))

            sub_str = "SPEED INCREASED • NEW CHALLENGES UNLOCKED"
            s_surf = self.font_banner_sub.render(sub_str, True, (240, 240, 255))
            surface.blit(s_surf, (bx + (bw - s_surf.get_width()) // 2, by + 40))
