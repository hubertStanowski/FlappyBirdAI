import pygame

# Dimensions
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 640

# Speed
SCROLL_SPEED = 3
GRAVITY = 0.5
FLAP_SPEED = 8

# Images
PLAYER_IMG = pygame.image.load("images/bird.png")
GROUND_IMG = pygame.image.load("images/ground.png")
BACKGROUND_IMG = pygame.image.load("images/background.png")
PIPE_IMG = pygame.image.load("images/pipe.png")


# Pipes
TOP = 1
BOTTOM = 0
PIPE_GAP = 150
PIPE_SEPERATION = 280


# Colors
WHITE = (255, 255, 255)
SKY_COLOR = (102, 178, 255)
