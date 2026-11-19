"""
Main Game Controller for Pixel Runner (Modern Edition).
Structured State Machine: MENU -> PLAYING -> PAUSED -> GAME_OVER.
Optimized for 60 FPS gameplay, responsive input, and dynamic effects.
"""
import random
import pygame
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    INITIAL_SPEED, MAX_SPEED, SPEED_INCREMENT, GROUND_Y
)
from src.sound_synth import SoundManager
from src.entities.player import Player, Particle
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
        self.coin_sparkles = []
        self.spawn_timer = 0
        self.screen_shake = 0
        self.running = True

        # Pre-allocated shake surface for high performance
        self.shake_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    def reset_game(self):
        self.player.reset()
        self.score_mgr.reset_current()
        self.obstacles.clear()
        self.coins.clear()
        self.coin_sparkles.clear()
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
        # Dynamic spawn cadence based on speed
        min_spawn_interval = max(50, int(105 - (self.speed - INITIAL_SPEED) * 5.2))
        
        if self.spawn_timer >= min_spawn_interval:
            self.spawn_timer = 0
            
            # 75% Obstacle spawn, 25% Coin pattern
            if random.random() < 0.75:
                # Drone spawns once speed exceeds 8.2
                if self.speed > 8.2 and random.random() < 0.38:
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
                coin_y = GROUND_Y - 35 if random.random() < 0.55 else GROUND_Y - 85
                count = random.randint(3, 4)
                for i in range(count):
                    self.coins.append(Coin(SCREEN_WIDTH + 50 + i * 36, coin_y))

    def update(self):
        if self.state != self.STATE_PLAYING:
            return

        keys = pygame.key.get_pressed()
        self.player.update(keys, speed_factor=self.speed)

        # Gradual speed progression
        if self.speed < MAX_SPEED:
            self.speed += SPEED_INCREMENT

        # Score increments with distance
        self.score_mgr.add_score(self.speed * 0.1)

        # Milestone chime every 1000 points
        if int(self.score_mgr.current_score) > 0 and int(self.score_mgr.current_score) % 1000 < 5:
            self.sound_mgr.play_checkpoint()

        self.background.update(self.speed)
        self.spawn_entities()

        # Update obstacles & collision
        player_rect = self.player.rect
        for obs in self.obstacles:
            obs.update(self.speed)
            if player_rect.colliderect(obs.rect):
                self.sound_mgr.play_hit()
                self.screen_shake = 16
                self.score_mgr.save_high_score()
                self.state = self.STATE_GAME_OVER
                break

        self.obstacles = [obs for obs in self.obstacles if not obs.is_offscreen()]

        # Update coins & pickup sparkle effect
        for coin in self.coins:
            coin.update(self.speed)
            if not coin.collected and player_rect.colliderect(coin.rect):
                coin.collected = True
                self.score_mgr.add_coin()
                self.sound_mgr.play_coin()

                # Golden pickup sparkle burst
                for _ in range(8):
                    self.coin_sparkles.append(Particle(
                        coin.x, coin.y,
                        random.uniform(-3, 3),
                        random.uniform(-3, 3),
                        random.choice([(255, 235, 80), (255, 255, 200), (0, 240, 255)]),
                        random.uniform(3, 6),
                        lifetime=18,
                        decay_rate=0.25
                    ))

        self.coins = [c for c in self.coins if not c.is_offscreen() and not c.collected]

        # Update coin sparkles
        for p in self.coin_sparkles:
            p.update()
        self.coin_sparkles = [p for p in self.coin_sparkles if p.is_alive()]

        # Decay screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1

    def draw(self):
        # Determine render target
        if self.screen_shake > 0:
            target_surf = self.shake_surface
        else:
            target_surf = self.screen

        # 1. Background
        self.background.draw(target_surf)

        # 2. Coins
        for coin in self.coins:
            coin.draw(target_surf)

        # 3. Coin Sparkle Particles
        for p in self.coin_sparkles:
            p.draw(target_surf)

        # 4. Obstacles
        for obs in self.obstacles:
            obs.draw(target_surf)

        # 5. Humanoid Player
        self.player.draw(target_surf)

        # 6. Modern HUD
        self.hud.draw(target_surf, self.score_mgr, self.speed)

        # 7. State Overlays
        if self.state == self.STATE_MENU:
            self.menu.draw_start_menu(target_surf)
        elif self.state == self.STATE_PAUSED:
            self.menu.draw_pause(target_surf)
        elif self.state == self.STATE_GAME_OVER:
            self.menu.draw_game_over(
                target_surf,
                self.score_mgr.current_score,
                self.score_mgr.high_score,
                self.score_mgr.coins
            )

        # Apply screen shake blit if active
        if self.screen_shake > 0:
            ox = random.randint(-self.screen_shake, self.screen_shake)
            oy = random.randint(-self.screen_shake, self.screen_shake)
            self.screen.fill((10, 8, 20))
            self.screen.blit(self.shake_surface, (ox, oy))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
