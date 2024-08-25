import pygame
from user_config import HUMAN_PLAYING
# Window dimensions
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 640

# Player starting position
PLAYER_X = WINDOW_WIDTH // 3
PLAYER_Y = WINDOW_HEIGHT // 2

# Font
FONT = None
SCORE_FONT_SIZE = 70
GENERATION_FONT_SIZE = 50
RESET_FONT_SIZE = 100
FPS_FONT_SIZE = 30
ALIVE_FONT_SIZE = FPS_FONT_SIZE
NODE_ID_FONT_SIZE = 22

# Speed
SCROLL_SPEED = 3
GRAVITY = 0.5
FLAP_SPEED = 8
FPS_LOWER_BOUND = 30
FPS_HIGHER_BOUND = 160

# Images
PLAYER_IMG = pygame.image.load("images/bird.png")
GROUND_IMG = pygame.image.load("images/ground.png")
BACKGROUND_IMG = pygame.image.load("images/background.png")
PIPE_IMG = pygame.image.load("images/pipe.png")

# Pipes
TOP = 1
BOTTOM = 0
PIPE_GAP = 98 if not HUMAN_PLAYING else 120
PIPE_SEPERATION = 280

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
