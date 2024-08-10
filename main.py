from constants import *
from player import Player
from pipe import Pipe

import pygame
import random


def main():
    pygame.init()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.display.set_caption("Flappy Bird AI")

    clock = pygame.time.Clock()
    player = Player(WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2)

    ground_scroll = 0
    flying = False

    while True:
        clock.tick(60)
        window.blit(BACKGROUND_IMG, (0, 0))
        window.blit(GROUND_IMG, (ground_scroll,
                    WINDOW_HEIGHT-GROUND_IMG.get_height()))

        player.draw(window)
        pygame.display.update()

        ground_scroll -= SCROLL_SPEED

        if abs(ground_scroll) > 50:
            ground_scroll = 0

        if flying:
            player.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flying = True
                    player.flap()


if __name__ == "__main__":
    main()
