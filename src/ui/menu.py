import math
import pygame
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_TEXT_MAIN, COLOR_TEXT_ACCENT,
    COLOR_TEXT_GOLD, COLOR_TEXT_MUTED
)

class Menu:
    def __init__(self):
        pygame.font.init()
        self.font_title = pygame.font.SysFont("Consolas", 52, bold=True)
        self.font_sub = pygame.font.SysFont("Consolas", 24, bold=True)
        self.font_body = pygame.font.SysFont("Consolas", 18)

    def draw_start_menu(self, surface):
        # Dim background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 8, 25, 200))
        surface.blit(overlay, (0, 0))

        # Title
        title_surf = self.font_title.render("PIXEL RUNNER", True, COLOR_TEXT_ACCENT)
        surface.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 120))

        sub_surf = self.font_body.render("PROJECT 01 — 2D ROADMAP", True, COLOR_TEXT_MUTED)
        surface.blit(sub_surf, (SCREEN_WIDTH // 2 - sub_surf.get_width() // 2, 180))

        # Blinking Start Text
        blink = math.sin(pygame.time.get_ticks() * 0.006) > 0
        if blink:
            start_surf = self.font_sub.render("PRESS SPACE TO PLAY", True, COLOR_TEXT_MAIN)
            surface.blit(start_surf, (SCREEN_WIDTH // 2 - start_surf.get_width() // 2, 260))

        # Controls Guide Box
        box_rect = pygame.Rect(SCREEN_WIDTH // 2 - 180, 330, 360, 110)
        pygame.draw.rect(surface, (25, 20, 45), box_rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_TEXT_MUTED, box_rect, 2, border_radius=8)

        c1 = self.font_body.render("SPACE / UP : Jump", True, COLOR_TEXT_MAIN)
        c2 = self.font_body.render("DOWN / S   : Slide / Duck", True, COLOR_TEXT_MAIN)
        c3 = self.font_body.render("ESC        : Pause Game", True, COLOR_TEXT_MAIN)

        surface.blit(c1, (box_rect.x + 35, box_rect.y + 16))
        surface.blit(c2, (box_rect.x + 35, box_rect.y + 45))
        surface.blit(c3, (box_rect.x + 35, box_rect.y + 74))

    def draw_pause(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        surface.blit(overlay, (0, 0))

        txt = self.font_title.render("PAUSED", True, COLOR_TEXT_ACCENT)
        surface.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, 200))

        txt2 = self.font_sub.render("Press ESC to Resume", True, COLOR_TEXT_MAIN)
        surface.blit(txt2, (SCREEN_WIDTH // 2 - txt2.get_width() // 2, 270))

    def draw_game_over(self, surface, score, high_score, coins):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 5, 15, 215))
        surface.blit(overlay, (0, 0))

        title = self.font_title.render("GAME OVER", True, (255, 60, 90))
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 110))

        sc = self.font_sub.render(f"Final Score: {int(score)}", True, COLOR_TEXT_MAIN)
        surface.blit(sc, (SCREEN_WIDTH // 2 - sc.get_width() // 2, 190))

        hi = self.font_sub.render(f"Best Score:  {int(high_score)}", True, COLOR_TEXT_GOLD)
        surface.blit(hi, (SCREEN_WIDTH // 2 - hi.get_width() // 2, 230))

        cn = self.font_body.render(f"Coins: {coins}", True, COLOR_TEXT_MUTED)
        surface.blit(cn, (SCREEN_WIDTH // 2 - cn.get_width() // 2, 270))

        blink = math.sin(pygame.time.get_ticks() * 0.007) > 0
        if blink:
            rst = self.font_sub.render("PRESS SPACE TO RESTART", True, COLOR_TEXT_ACCENT)
            surface.blit(rst, (SCREEN_WIDTH // 2 - rst.get_width() // 2, 340))
