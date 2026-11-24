"""
Modern Minimalist Glassmorphism Menus with Character Selection.
Allows selecting between 4 Subway Heroes: Jake, Tricky, Fresh, Yutani.
"""
import math
import pygame
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_TEXT_MAIN, COLOR_TEXT_ACCENT,
    COLOR_TEXT_GOLD, COLOR_TEXT_MUTED, COLOR_TEXT_DANGER,
    CHARACTERS
)
from src.ui.icons import (
    draw_trophy, draw_coin_icon, draw_runner_icon, draw_pause_icon
)

class Menu:
    def __init__(self):
        pygame.font.init()
        self.font_title = pygame.font.SysFont("Consolas", 42, bold=True)
        self.font_heading = pygame.font.SysFont("Consolas", 22, bold=True)
        self.font_body = pygame.font.SysFont("Consolas", 16, bold=True)
        self.font_small = pygame.font.SysFont("Consolas", 13)
        self.font_hero_name = pygame.font.SysFont("Consolas", 20, bold=True)
        self.font_hero_sub = pygame.font.SysFont("Consolas", 12, bold=True)

    def _draw_glass_panel(self, surface, rect, border_color=(0, 240, 255, 130), bg_color=(16, 12, 30, 225)):
        panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(panel, bg_color, (0, 0, rect.width, rect.height), border_radius=16)
        pygame.draw.rect(panel, border_color, (0, 0, rect.width, rect.height), width=2, border_radius=16)
        pygame.draw.line(panel, (255, 255, 255, 45), (16, 2), (rect.width - 16, 2), 2)
        surface.blit(panel, (rect.x, rect.y))

    def _draw_key_badge(self, surface, x, y, text, width=70):
        badge = pygame.Rect(x, y, width, 24)
        pygame.draw.rect(surface, (36, 28, 56), badge, border_radius=6)
        pygame.draw.rect(surface, (90, 75, 130), badge, width=1, border_radius=6)
        txt = self.font_small.render(text, True, COLOR_TEXT_ACCENT)
        surface.blit(txt, (badge.centerx - txt.get_width() // 2, badge.centery - txt.get_height() // 2))

    def draw_start_menu(self, surface, selected_char_idx=0, player_ref=None):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 6, 20, 215))
        surface.blit(overlay, (0, 0))

        # Main Glass Card
        card_w, card_h = 580, 430
        card_x = (SCREEN_WIDTH - card_w) // 2
        card_y = (SCREEN_HEIGHT - card_h) // 2 - 10
        card_rect = pygame.Rect(card_x, card_y, card_w, card_h)
        self._draw_glass_panel(surface, card_rect, border_color=(0, 240, 255, 140))

        # Title
        draw_runner_icon(surface, card_rect.centerx - 175, card_rect.y + 36, size=26, color=COLOR_TEXT_ACCENT)
        title_surf = self.font_title.render("PIXEL RUNNER", True, COLOR_TEXT_ACCENT)
        surface.blit(title_surf, (card_rect.centerx - title_surf.get_width() // 2 + 10, card_rect.y + 16))

        sub_surf = self.font_small.render("SUBWAY HEROES EDITION • CHOOSE YOUR RUNNER", True, COLOR_TEXT_MUTED)
        surface.blit(sub_surf, (card_rect.centerx - sub_surf.get_width() // 2, card_rect.y + 64))

        # ----------------------------------------------------
        # CHARACTER SELECTION CAROUSEL (Jake, Tricky, Fresh, Yutani)
        # ----------------------------------------------------
        char_data = CHARACTERS[selected_char_idx % len(CHARACTERS)]
        carousel_y = card_rect.y + 90
        carousel_box = pygame.Rect(card_rect.x + 35, carousel_y, card_w - 70, 115)
        pygame.draw.rect(surface, (24, 18, 42), carousel_box, border_radius=12)
        pygame.draw.rect(surface, char_data["accent_color"], carousel_box, width=2, border_radius=12)

        # Left / Right Arrow Selectors (Clickable or [Q] / [E])
        arrow_left = pygame.Rect(carousel_box.x + 12, carousel_box.centery - 16, 32, 32)
        pygame.draw.rect(surface, (38, 28, 62), arrow_left, border_radius=8)
        arr_l_txt = self.font_heading.render("<", True, char_data["accent_color"])
        surface.blit(arr_l_txt, (arrow_left.centerx - arr_l_txt.get_width() // 2, arrow_left.centery - arr_l_txt.get_height() // 2))

        arrow_right = pygame.Rect(carousel_box.right - 44, carousel_box.centery - 16, 32, 32)
        pygame.draw.rect(surface, (38, 28, 62), arrow_right, border_radius=8)
        arr_r_txt = self.font_heading.render(">", True, char_data["accent_color"])
        surface.blit(arr_r_txt, (arrow_right.centerx - arr_r_txt.get_width() // 2, arrow_right.centery - arr_r_txt.get_height() // 2))

        # Draw Character Preview inside Carousel Box
        char_preview_x = carousel_box.x + 95
        char_preview_y = carousel_box.bottom - 18
        if player_ref:
            # Temporarily draw preview at preview position
            orig_x, orig_y = player_ref.x, player_ref.y
            orig_grounded, orig_duck = player_ref.is_grounded, player_ref.is_ducking
            player_ref.x = char_preview_x
            player_ref.y = char_preview_y
            player_ref.is_grounded = True
            player_ref.is_ducking = False
            player_ref.draw(surface)
            player_ref.x = orig_x
            player_ref.y = orig_y
            player_ref.is_grounded = orig_grounded
            player_ref.is_ducking = orig_duck

        # Character Information
        name_txt = self.font_hero_name.render(char_data["name"], True, char_data["accent_color"])
        surface.blit(name_txt, (carousel_box.x + 145, carousel_box.y + 14))

        # Badge pill
        tag_rect = pygame.Rect(carousel_box.x + 145, carousel_box.y + 40, 195, 20)
        pygame.draw.rect(surface, (38, 26, 56), tag_rect, border_radius=10)
        tag_txt = self.font_hero_sub.render(char_data["title"], True, char_data["tag_color"])
        surface.blit(tag_txt, (tag_rect.centerx - tag_txt.get_width() // 2, tag_rect.centery - tag_txt.get_height() // 2))

        desc_txt = self.font_small.render(char_data["desc"], True, COLOR_TEXT_MUTED)
        surface.blit(desc_txt, (carousel_box.x + 145, carousel_box.y + 68))

        hint_txt = self.font_small.render("[Q] Prev  •  [E] Next", True, (140, 130, 170))
        surface.blit(hint_txt, (carousel_box.x + 145, carousel_box.y + 90))

        # ----------------------------------------------------
        # START BUTTON
        # ----------------------------------------------------
        pulse = (math.sin(pygame.time.get_ticks() * 0.007) + 1.0) * 0.5
        btn_w, btn_h = 320, 46
        btn_rect = pygame.Rect(card_rect.centerx - btn_w // 2, card_rect.y + 225, btn_w, btn_h)
        btn_bg = (0, int(180 + 60 * pulse), int(210 + 45 * pulse), 195)
        
        btn_surf = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
        pygame.draw.rect(btn_surf, btn_bg, (0, 0, btn_w, btn_h), border_radius=23)
        pygame.draw.rect(btn_surf, (255, 255, 255, int(150 * pulse)), (0, 0, btn_w, btn_h), width=2, border_radius=23)
        surface.blit(btn_surf, (btn_rect.x, btn_rect.y))

        play_txt = self.font_heading.render("PRESS SPACE TO PLAY", True, (15, 15, 30))
        surface.blit(play_txt, (btn_rect.centerx - play_txt.get_width() // 2, btn_rect.centery - play_txt.get_height() // 2))

        # ----------------------------------------------------
        # CONTROLS ROW
        # ----------------------------------------------------
        ctrl_y = card_rect.y + 290
        pygame.draw.line(surface, (50, 40, 80), (card_rect.x + 30, ctrl_y), (card_rect.right - 30, ctrl_y), 1)

        self._draw_key_badge(surface, card_rect.x + 50, ctrl_y + 12, "SPACE / W", width=95)
        txt_jump = self.font_body.render("Jump (Press 2x for Double Jump!)", True, COLOR_TEXT_MAIN)
        surface.blit(txt_jump, (card_rect.x + 165, ctrl_y + 15))

        self._draw_key_badge(surface, card_rect.x + 50, ctrl_y + 42, "DOWN / S", width=95)
        txt_slide = self.font_body.render("Low Slide under flying drones", True, COLOR_TEXT_MAIN)
        surface.blit(txt_slide, (card_rect.x + 165, ctrl_y + 45))

        self._draw_key_badge(surface, card_rect.x + 50, ctrl_y + 72, "Q / E", width=95)
        txt_char = self.font_body.render("Switch Subway Runner Hero", True, char_data["accent_color"])
        surface.blit(txt_char, (card_rect.x + 165, ctrl_y + 75))

        self._draw_key_badge(surface, card_rect.x + 50, ctrl_y + 102, "ESC", width=95)
        txt_pause = self.font_body.render("Pause & Resume gameplay", True, COLOR_TEXT_MUTED)
        surface.blit(txt_pause, (card_rect.x + 165, ctrl_y + 105))

    def draw_pause(self, surface, char_data=None):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 6, 18, 190))
        surface.blit(overlay, (0, 0))

        card_w, card_h = 380, 220
        card_rect = pygame.Rect((SCREEN_WIDTH - card_w) // 2, (SCREEN_HEIGHT - card_h) // 2, card_w, card_h)
        accent = char_data["accent_color"] if char_data else (0, 240, 255)
        self._draw_glass_panel(surface, card_rect, border_color=(accent[0], accent[1], accent[2], 130))

        draw_pause_icon(surface, card_rect.centerx, card_rect.y + 42, size=24, color=accent)

        txt = self.font_heading.render("GAME PAUSED", True, COLOR_TEXT_MAIN)
        surface.blit(txt, (card_rect.centerx - txt.get_width() // 2, card_rect.y + 72))

        if char_data:
            c_txt = self.font_small.render(f"Runner: {char_data['name']}", True, char_data['accent_color'])
            surface.blit(c_txt, (card_rect.centerx - c_txt.get_width() // 2, card_rect.y + 110))

        txt2 = self.font_body.render("Press ESC to Resume", True, COLOR_TEXT_MUTED)
        surface.blit(txt2, (card_rect.centerx - txt2.get_width() // 2, card_rect.y + 145))

    def draw_game_over(self, surface, score, high_score, coins, char_data=None):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((22, 6, 16, 215))
        surface.blit(overlay, (0, 0))

        card_w, card_h = 480, 370
        card_rect = pygame.Rect((SCREEN_WIDTH - card_w) // 2, (SCREEN_HEIGHT - card_h) // 2, card_w, card_h)
        self._draw_glass_panel(surface, card_rect, border_color=(255, 75, 110, 160), bg_color=(24, 10, 22, 235))

        title = self.font_title.render("GAME OVER", True, COLOR_TEXT_DANGER)
        surface.blit(title, (card_rect.centerx - title.get_width() // 2, card_rect.y + 20))

        if char_data:
            c_txt = self.font_small.render(f"Runner: {char_data['name']} ({char_data['title']})", True, char_data['accent_color'])
            surface.blit(c_txt, (card_rect.centerx - c_txt.get_width() // 2, card_rect.y + 68))

        # Score Row
        score_box = pygame.Rect(card_rect.x + 40, card_rect.y + 95, card_w - 80, 46)
        pygame.draw.rect(surface, (38, 16, 32), score_box, border_radius=10)
        pygame.draw.rect(surface, (80, 30, 50), score_box, width=1, border_radius=10)
        sc_lbl = self.font_body.render("Final Score", True, COLOR_TEXT_MUTED)
        sc_val = self.font_heading.render(f"{int(score):06d}", True, COLOR_TEXT_MAIN)
        surface.blit(sc_lbl, (score_box.x + 20, score_box.centery - sc_lbl.get_height() // 2))
        surface.blit(sc_val, (score_box.right - sc_val.get_width() - 20, score_box.centery - sc_val.get_height() // 2))

        # High Score Row
        hi_box = pygame.Rect(card_rect.x + 40, card_rect.y + 150, card_w - 80, 46)
        pygame.draw.rect(surface, (38, 25, 20), hi_box, border_radius=10)
        pygame.draw.rect(surface, (90, 60, 20), hi_box, width=1, border_radius=10)
        draw_trophy(surface, hi_box.x + 30, hi_box.centery, size=20, color=COLOR_TEXT_GOLD)
        hi_lbl = self.font_body.render("Best Record", True, COLOR_TEXT_GOLD)
        hi_val = self.font_heading.render(f"{int(high_score):06d}", True, COLOR_TEXT_GOLD)
        surface.blit(hi_lbl, (hi_box.x + 55, hi_box.centery - hi_lbl.get_height() // 2))
        surface.blit(hi_val, (hi_box.right - hi_val.get_width() - 20, hi_box.centery - hi_val.get_height() // 2))

        # Coins Row
        draw_coin_icon(surface, card_rect.centerx - 55, card_rect.y + 225, size=22)
        cn_txt = self.font_body.render(f"Coins: {coins}", True, COLOR_TEXT_GOLD)
        surface.blit(cn_txt, (card_rect.centerx - 28, card_rect.y + 215))

        # Restart Prompt Button
        pulse = (math.sin(pygame.time.get_ticks() * 0.008) + 1.0) * 0.5
        rst_btn = pygame.Rect(card_rect.centerx - 160, card_rect.y + 280, 320, 44)
        btn_bg = (0, int(190 + 50 * pulse), int(220 + 35 * pulse), 200)
        
        btn_surf = pygame.Surface((rst_btn.width, rst_btn.height), pygame.SRCALPHA)
        pygame.draw.rect(btn_surf, btn_bg, (0, 0, rst_btn.width, rst_btn.height), border_radius=22)
        pygame.draw.rect(btn_surf, (255, 255, 255, int(140 * pulse)), (0, 0, rst_btn.width, rst_btn.height), width=2, border_radius=22)
        surface.blit(btn_surf, (rst_btn.x, rst_btn.y))

        rst_txt = self.font_heading.render("PRESS SPACE TO RESTART", True, (15, 15, 30))
        surface.blit(rst_txt, (rst_btn.centerx - rst_txt.get_width() // 2, rst_btn.centery - rst_txt.get_height() // 2))
