"""
Modern Minimalist Glassmorphism Menus & Overlays.
Designed with frosted translucent cards, vector icons, and clear typography.
"""
import math
import pygame
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_TEXT_MAIN, COLOR_TEXT_ACCENT,
    COLOR_TEXT_GOLD, COLOR_TEXT_MUTED, COLOR_TEXT_DANGER
)
from src.ui.icons import (
    draw_trophy, draw_coin_icon, draw_runner_icon, draw_pause_icon
)

class Menu:
    def __init__(self):
        pygame.font.init()
        self.font_title = pygame.font.SysFont("Consolas", 46, bold=True)
        self.font_heading = pygame.font.SysFont("Consolas", 24, bold=True)
        self.font_body = pygame.font.SysFont("Consolas", 17, bold=True)
        self.font_small = pygame.font.SysFont("Consolas", 14)

    def _draw_glass_panel(self, surface, rect, border_color=(0, 240, 255, 130), bg_color=(16, 12, 30, 225)):
        """Draws frosted glass backdrop card."""
        panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(panel, bg_color, (0, 0, rect.width, rect.height), border_radius=16)
        pygame.draw.rect(panel, border_color, (0, 0, rect.width, rect.height), width=2, border_radius=16)
        # Top highlight sheen
        pygame.draw.line(panel, (255, 255, 255, 50), (16, 2), (rect.width - 16, 2), 2)
        surface.blit(panel, (rect.x, rect.y))

    def _draw_key_badge(self, surface, x, y, text, width=70):
        """Draws modern keyboard keycap badge."""
        badge = pygame.Rect(x, y, width, 26)
        pygame.draw.rect(surface, (38, 30, 60), badge, border_radius=6)
        pygame.draw.rect(surface, (90, 75, 130), badge, width=1, border_radius=6)
        txt = self.font_small.render(text, True, COLOR_TEXT_ACCENT)
        surface.blit(txt, (badge.centerx - txt.get_width() // 2, badge.centery - txt.get_height() // 2))

    def draw_start_menu(self, surface):
        # 1. Dark frosted overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 8, 22, 210))
        surface.blit(overlay, (0, 0))

        # 2. Main Glass Card
        card_w, card_h = 520, 360
        card_x = (SCREEN_WIDTH - card_w) // 2
        card_y = (SCREEN_HEIGHT - card_h) // 2
        card_rect = pygame.Rect(card_x, card_y, card_w, card_h)
        self._draw_glass_panel(surface, card_rect, border_color=(0, 240, 255, 140))

        # 3. Title with Runner Icon
        draw_runner_icon(surface, card_rect.centerx - 170, card_rect.y + 48, size=28, color=COLOR_TEXT_ACCENT)
        title_surf = self.font_title.render("PIXEL RUNNER", True, COLOR_TEXT_ACCENT)
        surface.blit(title_surf, (card_rect.centerx - title_surf.get_width() // 2 + 10, card_rect.y + 26))

        sub_surf = self.font_small.render("MODERN HUMAN EDITION • PROJECT 01", True, COLOR_TEXT_MUTED)
        surface.blit(sub_surf, (card_rect.centerx - sub_surf.get_width() // 2, card_rect.y + 82))

        # 4. Animated Play Prompt Button
        pulse = (math.sin(pygame.time.get_ticks() * 0.007) + 1.0) * 0.5
        btn_w, btn_h = 320, 48
        btn_rect = pygame.Rect(card_rect.centerx - btn_w // 2, card_rect.y + 120, btn_w, btn_h)
        btn_bg = (0, int(180 + 60 * pulse), int(210 + 45 * pulse), 190)
        
        btn_surf = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
        pygame.draw.rect(btn_surf, btn_bg, (0, 0, btn_w, btn_h), border_radius=24)
        pygame.draw.rect(btn_surf, (255, 255, 255, int(150 * pulse)), (0, 0, btn_w, btn_h), width=2, border_radius=24)
        surface.blit(btn_surf, (btn_rect.x, btn_rect.y))

        play_txt = self.font_heading.render("PRESS SPACE TO PLAY", True, (15, 15, 30))
        surface.blit(play_txt, (btn_rect.centerx - play_txt.get_width() // 2, btn_rect.centery - play_txt.get_height() // 2))

        # 5. Controls Section Box
        ctrl_y = card_rect.y + 195
        pygame.draw.line(surface, (50, 40, 80), (card_rect.x + 30, ctrl_y), (card_rect.right - 30, ctrl_y), 1)

        # Control Row 1: Jump
        self._draw_key_badge(surface, card_rect.x + 60, ctrl_y + 15, "SPACE / W", width=95)
        txt_jump = self.font_body.render("Jump & Vault over spikes", True, COLOR_TEXT_MAIN)
        surface.blit(txt_jump, (card_rect.x + 175, ctrl_y + 19))

        # Control Row 2: Slide
        self._draw_key_badge(surface, card_rect.x + 60, ctrl_y + 52, "DOWN / S", width=95)
        txt_slide = self.font_body.render("Low Slide under drones", True, COLOR_TEXT_MAIN)
        surface.blit(txt_slide, (card_rect.x + 175, ctrl_y + 56))

        # Control Row 3: Pause
        self._draw_key_badge(surface, card_rect.x + 60, ctrl_y + 89, "ESC", width=95)
        txt_pause = self.font_body.render("Pause & Resume game", True, COLOR_TEXT_MAIN)
        surface.blit(txt_pause, (card_rect.x + 175, ctrl_y + 93))

    def draw_pause(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 6, 18, 190))
        surface.blit(overlay, (0, 0))

        card_w, card_h = 360, 200
        card_rect = pygame.Rect((SCREEN_WIDTH - card_w) // 2, (SCREEN_HEIGHT - card_h) // 2, card_w, card_h)
        self._draw_glass_panel(surface, card_rect, border_color=(0, 240, 255, 120))

        draw_pause_icon(surface, card_rect.centerx, card_rect.y + 45, size=24, color=COLOR_TEXT_ACCENT)

        txt = self.font_heading.render("GAME PAUSED", True, COLOR_TEXT_MAIN)
        surface.blit(txt, (card_rect.centerx - txt.get_width() // 2, card_rect.y + 75))

        txt2 = self.font_body.render("Press ESC to Resume", True, COLOR_TEXT_MUTED)
        surface.blit(txt2, (card_rect.centerx - txt2.get_width() // 2, card_rect.y + 120))

    def draw_game_over(self, surface, score, high_score, coins):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((22, 6, 16, 215))
        surface.blit(overlay, (0, 0))

        card_w, card_h = 480, 360
        card_rect = pygame.Rect((SCREEN_WIDTH - card_w) // 2, (SCREEN_HEIGHT - card_h) // 2, card_w, card_h)
        self._draw_glass_panel(surface, card_rect, border_color=(255, 75, 110, 160), bg_color=(24, 10, 22, 235))

        title = self.font_title.render("GAME OVER", True, COLOR_TEXT_DANGER)
        surface.blit(title, (card_rect.centerx - title.get_width() // 2, card_rect.y + 25))

        # Score Row
        score_box = pygame.Rect(card_rect.x + 40, card_rect.y + 95, card_w - 80, 48)
        pygame.draw.rect(surface, (38, 16, 32), score_box, border_radius=10)
        pygame.draw.rect(surface, (80, 30, 50), score_box, width=1, border_radius=10)
        sc_lbl = self.font_body.render("Final Score", True, COLOR_TEXT_MUTED)
        sc_val = self.font_heading.render(f"{int(score):06d}", True, COLOR_TEXT_MAIN)
        surface.blit(sc_lbl, (score_box.x + 20, score_box.centery - sc_lbl.get_height() // 2))
        surface.blit(sc_val, (score_box.right - sc_val.get_width() - 20, score_box.centery - sc_val.get_height() // 2))

        # High Score Row
        hi_box = pygame.Rect(card_rect.x + 40, card_rect.y + 155, card_w - 80, 48)
        pygame.draw.rect(surface, (38, 25, 20), hi_box, border_radius=10)
        pygame.draw.rect(surface, (90, 60, 20), hi_box, width=1, border_radius=10)
        draw_trophy(surface, hi_box.x + 30, hi_box.centery, size=20, color=COLOR_TEXT_GOLD)
        hi_lbl = self.font_body.render("Best Record", True, COLOR_TEXT_GOLD)
        hi_val = self.font_heading.render(f"{int(high_score):06d}", True, COLOR_TEXT_GOLD)
        surface.blit(hi_lbl, (hi_box.x + 55, hi_box.centery - hi_lbl.get_height() // 2))
        surface.blit(hi_val, (hi_box.right - hi_val.get_width() - 20, hi_box.centery - hi_val.get_height() // 2))

        # Coins Row
        draw_coin_icon(surface, card_rect.centerx - 45, card_rect.y + 230, size=22)
        cn_txt = self.font_body.render(f"Coins Collected: {coins}", True, COLOR_TEXT_GOLD)
        surface.blit(cn_txt, (card_rect.centerx - 20, card_rect.y + 220))

        # Restart Prompt Button
        pulse = (math.sin(pygame.time.get_ticks() * 0.008) + 1.0) * 0.5
        rst_btn = pygame.Rect(card_rect.centerx - 160, card_rect.y + 275, 320, 44)
        btn_bg = (0, int(190 + 50 * pulse), int(220 + 35 * pulse), 200)
        
        btn_surf = pygame.Surface((rst_btn.width, rst_btn.height), pygame.SRCALPHA)
        pygame.draw.rect(btn_surf, btn_bg, (0, 0, rst_btn.width, rst_btn.height), border_radius=22)
        pygame.draw.rect(btn_surf, (255, 255, 255, int(140 * pulse)), (0, 0, rst_btn.width, rst_btn.height), width=2, border_radius=22)
        surface.blit(btn_surf, (rst_btn.x, rst_btn.y))

        rst_txt = self.font_heading.render("PRESS SPACE TO RESTART", True, (15, 15, 30))
        surface.blit(rst_txt, (rst_btn.centerx - rst_txt.get_width() // 2, rst_btn.centery - rst_txt.get_height() // 2))
