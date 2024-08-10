import pygame


WINDOW_WIDTH = 480
WINDOW_HEIGHT = 640

SCROLL_SPEED = 3
GRAVITY = 0.5

PLAYER_IMG = pygame.image.load("images/bird.png")
GROUND_IMG = pygame.image.load("images/ground.png")
BACKGROUND_IMG = pygame.image.load("images/background.png")
PIPE_IMG = pygame.image.load("images/pipe.png")


# labels for position in Pipe
TOP = 1
BOTTOM = 0
PIPE_GAP = 150


WHITE = (255, 255, 255)
SKY_COLOR = (102, 178, 255)
