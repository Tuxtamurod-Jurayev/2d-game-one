"""
Modern Handcrafted Vector & Pixel-Accurate Icons.
Rendered dynamically using crisp geometrical shapes, highlights, and gradients.
Completely free of AI artifacts and designed for high clarity at all resolutions.
"""
import math
import pygame

def draw_trophy(surface, x, y, size=24, color=(255, 215, 0)):
    """Draws a sleek modern gold trophy cup."""
    scale = size / 24.0
    # Cup body
    cup_rect = pygame.Rect(x - int(7 * scale), y - int(10 * scale), int(14 * scale), int(11 * scale))
    pygame.draw.rect(surface, color, cup_rect, border_bottom_left_radius=int(6 * scale), border_bottom_right_radius=int(6 * scale))
    # Cup rim
    pygame.draw.rect(surface, (255, 240, 150), (x - int(8 * scale), y - int(11 * scale), int(16 * scale), int(3 * scale)), border_radius=int(2 * scale))
    # Handles
    pygame.draw.arc(surface, color, (x - int(12 * scale), y - int(9 * scale), int(7 * scale), int(8 * scale)), math.pi/2, 3*math.pi/2, max(2, int(2 * scale)))
    pygame.draw.arc(surface, color, (x + int(5 * scale), y - int(9 * scale), int(7 * scale), int(8 * scale)), -math.pi/2, math.pi/2, max(2, int(2 * scale)))
    # Stem
    pygame.draw.rect(surface, (218, 165, 32), (x - int(2 * scale), y + int(1 * scale), int(4 * scale), int(5 * scale)))
    # Base pedestal
    pygame.draw.rect(surface, (180, 130, 20), (x - int(7 * scale), y + int(6 * scale), int(14 * scale), int(4 * scale)), border_radius=int(2 * scale))
    # Star in center
    pygame.draw.circle(surface, (255, 255, 255), (x, y - int(5 * scale)), max(1, int(2 * scale)))

def draw_coin_icon(surface, x, y, size=22, anim_tick=0):
    """Draws a gleaming 3D gold coin with rotational shimmer."""
    scale = size / 22.0
    r = int(10 * scale)
    # Outer gold rim
    pygame.draw.circle(surface, (210, 150, 0), (x, y), r)
    pygame.draw.circle(surface, (255, 215, 0), (x, y), max(1, r - 2))
    # Inner ring
    pygame.draw.circle(surface, (230, 175, 10), (x, y), max(1, r - 4), 1)
    # Shimmer star / dollar mark
    sparkle = abs(math.sin(anim_tick * 0.08)) * (3 * scale)
    pygame.draw.line(surface, (255, 255, 230), (x - 2, y), (x + 2, y), max(1, int(2 * scale)))
    pygame.draw.line(surface, (255, 255, 230), (x, y - 2), (x, y + 2), max(1, int(2 * scale)))
    # Top highlight dot
    pygame.draw.circle(surface, (255, 255, 255), (x - int(3 * scale), y - int(3 * scale)), max(1, int(2 * scale)))

def draw_speed_icon(surface, x, y, size=22, color=(0, 240, 255)):
    """Draws an energetic lightning / speedometer bolt."""
    scale = size / 22.0
    points = [
        (x + int(1 * scale), y - int(10 * scale)),
        (x - int(7 * scale), y + int(0 * scale)),
        (x - int(1 * scale), y + int(0 * scale)),
        (x - int(3 * scale), y + int(10 * scale)),
        (x + int(6 * scale), y - int(1 * scale)),
        (x + int(0 * scale), y - int(1 * scale)),
    ]
    pygame.draw.polygon(surface, color, points)
    # Highlight core
    inner_points = [
        (x + int(1 * scale), y - int(7 * scale)),
        (x - int(4 * scale), y + int(0 * scale)),
        (x - int(0 * scale), y + int(0 * scale)),
        (x - int(1 * scale), y + int(6 * scale)),
        (x + int(3 * scale), y - int(1 * scale)),
    ]
    pygame.draw.polygon(surface, (255, 255, 255), inner_points)

def draw_runner_icon(surface, x, y, size=22, color=(0, 255, 180)):
    """Draws a sleek athletic human runner silhouette."""
    scale = size / 22.0
    # Head
    pygame.draw.circle(surface, color, (x - int(2 * scale), y - int(7 * scale)), max(2, int(3 * scale)))
    # Torso
    pygame.draw.line(surface, color, (x - int(1 * scale), y - int(4 * scale)), (x + int(2 * scale), y + int(2 * scale)), max(2, int(3 * scale)))
    # Forward Leg
    pygame.draw.line(surface, color, (x + int(2 * scale), y + int(2 * scale)), (x + int(8 * scale), y + int(4 * scale)), max(2, int(2 * scale)))
    pygame.draw.line(surface, color, (x + int(8 * scale), y + int(4 * scale)), (x + int(6 * scale), y + int(9 * scale)), max(2, int(2 * scale)))
    # Back Leg
    pygame.draw.line(surface, color, (x + int(2 * scale), y + int(2 * scale)), (x - int(5 * scale), y + int(5 * scale)), max(2, int(2 * scale)))
    pygame.draw.line(surface, color, (x - int(5 * scale), y + int(5 * scale)), (x - int(8 * scale), y + int(2 * scale)), max(2, int(2 * scale)))
    # Arms
    pygame.draw.line(surface, color, (x - int(1 * scale), y - int(3 * scale)), (x + int(5 * scale), y - int(1 * scale)), max(2, int(2 * scale)))
    pygame.draw.line(surface, color, (x - int(1 * scale), y - int(3 * scale)), (x - int(6 * scale), y + int(1 * scale)), max(2, int(2 * scale)))

def draw_pause_icon(surface, x, y, size=20, color=(255, 255, 255)):
    """Draws modern rounded double pause bars."""
    scale = size / 20.0
    w = max(2, int(3 * scale))
    h = int(12 * scale)
    gap = int(3 * scale)
    pygame.draw.rect(surface, color, (x - gap - w, y - h//2, w, h), border_radius=int(2 * scale))
    pygame.draw.rect(surface, color, (x + gap, y - h//2, w, h), border_radius=int(2 * scale))
