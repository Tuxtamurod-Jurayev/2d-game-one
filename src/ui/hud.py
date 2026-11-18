import pygame
from src.settings import (
    SCREEN_WIDTH, COLOR_TEXT_MAIN, COLOR_TEXT_ACCENT,
    COLOR_TEXT_GOLD, COLOR_TEXT_MUTED
)

class HUD:
    def __init__(self):
        pygame.font.init()
        self.font_main = pygame.font.SysFont("Consolas", 22, bold=True)
        self.font_small = pygame.font.SysFont("Consolas", 16)

    def draw(self, surface, score_mgr, speed):
        # 1. Current Score
        score_text = f"SCORE: {int(score_mgr.current_score):06d}"
        score_surf = self.font_main.render(score_text, True, COLOR_TEXT_MAIN)
        surface.blit(score_surf, (25, 20))

        # 2. High Score
        hi_text = f"HI-SCORE: {int(score_mgr.high_score):06d}"
        hi_surf = self.font_main.render(hi_text, True, COLOR_TEXT_ACCENT)
        surface.blit(hi_surf, (SCREEN_WIDTH - hi_surf.get_width() - 25, 20))

        # 3. Coins Collected
        coins_text = f"COINS: {score_mgr.coins}"
        coins_surf = self.font_main.render(coins_text, True, COLOR_TEXT_GOLD)
        surface.blit(coins_surf, (25, 52))

        # 4. Current Speed Indicator
        speed_text = f"SPEED: {speed:.1f}x"
        speed_surf = self.font_small.render(speed_text, True, COLOR_TEXT_MUTED)
        surface.blit(speed_surf, (SCREEN_WIDTH - speed_surf.get_width() - 25, 52))
