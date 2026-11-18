import random
import pygame
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    INITIAL_SPEED, MAX_SPEED, SPEED_INCREMENT, GROUND_Y
)
from src.sound_synth import SoundManager
from src.entities.player import Player
from src.entities.obstacle import Obstacle
from src.entities.coin import Coin
from src.world.background import Background
from src.ui.hud import HUD
from src.ui.menu import Menu
from src.managers.score_manager import ScoreManager

class Game:
    STATE_MENU = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    STATE_GAME_OVER = 3

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.sound_mgr = SoundManager()
        self.score_mgr = ScoreManager()
        self.background = Background()
        self.hud = HUD()
        self.menu = Menu()
        self.player = Player()

        self.state = self.STATE_MENU
        self.speed = INITIAL_SPEED
        self.obstacles = []
        self.coins = []
        self.spawn_timer = 0
        self.screen_shake = 0
        self.running = True

    def reset_game(self):
        self.player.reset()
        self.score_mgr.reset_current()
        self.obstacles.clear()
        self.coins.clear()
        self.speed = INITIAL_SPEED
        self.spawn_timer = 0
        self.screen_shake = 0
        self.state = self.STATE_PLAYING

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if self.state == self.STATE_MENU:
                    if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_RETURN):
                        self.reset_game()

                elif self.state == self.STATE_PLAYING:
                    if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                        self.player.jump(self.sound_mgr)
                    elif event.key == pygame.K_ESCAPE:
                        self.state = self.STATE_PAUSED

                elif self.state == self.STATE_PAUSED:
                    if event.key == pygame.K_ESCAPE:
                        self.state = self.STATE_PLAYING

                elif self.state == self.STATE_GAME_OVER:
                    if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_RETURN):
                        self.reset_game()

    def spawn_entities(self):
        self.spawn_timer += 1
        # Minimum distance based on speed
        min_spawn_interval = max(55, int(110 - (self.speed - INITIAL_SPEED) * 5))
        
        if self.spawn_timer >= min_spawn_interval:
            self.spawn_timer = 0
            
            # 75% Obstacle, 25% Coin row
            roll = random.random()
            if roll < 0.75:
                # Choose obstacle type
                if self.speed > 8.5 and random.random() < 0.35:
                    obs_type = Obstacle.TYPE_FLYING_DRONE
                else:
                    obs_type = random.choice([
                        Obstacle.TYPE_SMALL_GROUND,
                        Obstacle.TYPE_LARGE_GROUND,
                        Obstacle.TYPE_DOUBLE_GROUND
                    ])
                self.obstacles.append(Obstacle(obs_type, SCREEN_WIDTH + 50))
            else:
                # Spawn coin arc or row
                coin_y = GROUND_Y - 30 if random.random() < 0.5 else GROUND_Y - 80
                for i in range(3):
                    self.coins.append(Coin(SCREEN_WIDTH + 50 + i * 40, coin_y))

    def update(self):
        if self.state != self.STATE_PLAYING:
            return

        keys = pygame.key.get_pressed()
        self.player.update(keys)

        # Speed progression
        if self.speed < MAX_SPEED:
            self.speed += SPEED_INCREMENT

        # Score increments by travel distance
        self.score_mgr.add_score(self.speed * 0.1)

        # Milestone chime every 1000 pts
        if int(self.score_mgr.current_score) > 0 and int(self.score_mgr.current_score) % 1000 < 5:
            self.sound_mgr.play_checkpoint()

        self.background.update(self.speed)
        self.spawn_entities()

        # Update obstacles
        player_rect = self.player.rect
        for obs in self.obstacles:
            obs.update(self.speed)
            # Collision check
            if player_rect.colliderect(obs.rect):
                self.sound_mgr.play_hit()
                self.screen_shake = 18
                self.score_mgr.save_high_score()
                self.state = self.STATE_GAME_OVER
                break

        self.obstacles = [obs for obs in self.obstacles if not obs.is_offscreen()]

        # Update coins
        for coin in self.coins:
            coin.update(self.speed)
            if not coin.collected and player_rect.colliderect(coin.rect):
                coin.collected = True
                self.score_mgr.add_coin()
                self.sound_mgr.play_coin()

        self.coins = [c for c in self.coins if not c.is_offscreen() and not c.collected]

        # Decay screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1

    def draw(self):
        # Apply screen shake offset if active
        shake_x = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        shake_y = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0

        draw_surf = self.screen
        if shake_x != 0 or shake_y != 0:
            draw_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        # 1. Background
        self.background.draw(draw_surf)

        # 2. Coins
        for coin in self.coins:
            coin.draw(draw_surf)

        # 3. Obstacles
        for obs in self.obstacles:
            obs.draw(draw_surf)

        # 4. Player
        self.player.draw(draw_surf)

        # 5. HUD
        self.hud.draw(draw_surf, self.score_mgr, self.speed)

        # 6. Overlays
        if self.state == self.STATE_MENU:
            self.menu.draw_start_menu(draw_surf)
        elif self.state == self.STATE_PAUSED:
            self.menu.draw_pause(draw_surf)
        elif self.state == self.STATE_GAME_OVER:
            self.menu.draw_game_over(
                draw_surf,
                self.score_mgr.current_score,
                self.score_mgr.high_score,
                self.score_mgr.coins
            )

        if shake_x != 0 or shake_y != 0:
            self.screen.fill((0, 0, 0))
            self.screen.blit(draw_surf, (shake_x, shake_y))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
