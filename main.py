from constants import *
from player import Player

import pygame


def main():
    pygame.init()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.display.set_caption("Flappy Bird AI")

    clock = pygame.time.Clock()
    player = Player(WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2)

    while True:
        clock.tick(60)
        window.blit(BACKGROUND_IMG, (0, 0))

        player.draw(window)
        pygame.display.update()

        player.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.flap()


if __name__ == "__main__":
    main()
