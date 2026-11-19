"""
Modern Minimalist Translucent HUD with Handcrafted Vector Badges.
Provides high legibility and sleek frosted-glass aesthetics.
"""
import pygame
from src.settings import (
    SCREEN_WIDTH, COLOR_TEXT_MAIN, COLOR_TEXT_ACCENT,
    COLOR_TEXT_GOLD, COLOR_TEXT_MUTED
)
from src.ui.icons import (
    draw_trophy, draw_coin_icon, draw_speed_icon, draw_runner_icon
)

class HUD:
    def __init__(self):
        pygame.font.init()
        self.font_main = pygame.font.SysFont("Consolas", 20, bold=True)
        self.font_small = pygame.font.SysFont("Consolas", 15, bold=True)
        self.tick = 0

    def draw_glass_pill(self, surface, rect, border_color=(0, 240, 255, 90), bg_color=(18, 14, 34, 185)):
        """Draws a modern translucent pill-shaped badge with subtle border glow."""
        badge = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(badge, bg_color, (0, 0, rect.width, rect.height), border_radius=rect.height // 2)
        pygame.draw.rect(badge, border_color, (0, 0, rect.width, rect.height), width=1, border_radius=rect.height // 2)
        # Top subtle highlight line
        pygame.draw.line(badge, (255, 255, 255, 40), (rect.height // 2, 1), (rect.width - rect.height // 2, 1), 1)
        surface.blit(badge, (rect.x, rect.y))

    def draw(self, surface, score_mgr, speed):
        self.tick += 1

        # ----------------------------------------------------
        # 1. SCORE BADGE (Top Left)
        # ----------------------------------------------------
        score_val = f"{int(score_mgr.current_score):06d}"
        score_rect = pygame.Rect(20, 18, 175, 36)
        self.draw_glass_pill(surface, score_rect, border_color=(0, 255, 180, 100))
        # Runner icon
        draw_runner_icon(surface, score_rect.x + 22, score_rect.centery, size=18, color=(0, 255, 180))
        # Text
        score_txt = self.font_main.render(score_val, True, COLOR_TEXT_MAIN)
        surface.blit(score_txt, (score_rect.x + 40, score_rect.centery - score_txt.get_height() // 2))

        # ----------------------------------------------------
        # 2. COINS BADGE (Top Center)
        # ----------------------------------------------------
        coins_rect = pygame.Rect(SCREEN_WIDTH // 2 - 65, 18, 130, 36)
        self.draw_glass_pill(surface, coins_rect, border_color=(255, 215, 0, 110))
        # Animated coin icon
        draw_coin_icon(surface, coins_rect.x + 24, coins_rect.centery, size=20, anim_tick=self.tick)
        # Coins text
        coins_txt = self.font_main.render(f"x {score_mgr.coins}", True, COLOR_TEXT_GOLD)
        surface.blit(coins_txt, (coins_rect.x + 44, coins_rect.centery - coins_txt.get_height() // 2))

        # ----------------------------------------------------
        # 3. HIGH-SCORE BADGE (Top Right - Left of Speed)
        # ----------------------------------------------------
        hi_val = f"{int(score_mgr.high_score):06d}"
        hi_rect = pygame.Rect(SCREEN_WIDTH - 305, 18, 160, 36)
        self.draw_glass_pill(surface, hi_rect, border_color=(255, 180, 50, 100))
        # Trophy icon
        draw_trophy(surface, hi_rect.x + 22, hi_rect.centery, size=18, color=COLOR_TEXT_GOLD)
        # Hi-Score text
        hi_txt = self.font_small.render(hi_val, True, COLOR_TEXT_GOLD)
        surface.blit(hi_txt, (hi_rect.x + 40, hi_rect.centery - hi_txt.get_height() // 2))

        # ----------------------------------------------------
        # 4. SPEED METER BADGE (Top Right)
        # ----------------------------------------------------
        speed_rect = pygame.Rect(SCREEN_WIDTH - 130, 18, 110, 36)
        self.draw_glass_pill(surface, speed_rect, border_color=(0, 240, 255, 100))
        # Speed bolt icon
        draw_speed_icon(surface, speed_rect.x + 20, speed_rect.centery, size=18, color=COLOR_TEXT_ACCENT)
        # Speed text
        speed_txt = self.font_small.render(f"{speed:.1f}x", True, COLOR_TEXT_ACCENT)
        surface.blit(speed_txt, (speed_rect.x + 38, speed_rect.centery - speed_txt.get_height() // 2))
