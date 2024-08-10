from constants import *
from player import Player

import pygame


def main():
    pygame.init()
    display_info = pygame.display.Info()
    window = pygame.display.set_mode(
        (display_info.current_w, display_info.current_h))

    pygame.display.set_caption("Flappy Bird AI")

    clock = pygame.time.Clock()
    player = Player(100, 100)

    while True:
        clock.tick(60)

        window.fill(WHITE)
        player.draw(window)
        pygame.display.update()
        player.move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.flap()


if __name__ == "__main__":
    main()
