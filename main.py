from constants import *
from player import Player

import pygame


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.display.set_caption("Flappy Bird AI")

    clock = pygame.time.Clock()
    player = Player(WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2)
    ground_scroll = 0
    started = False

    while True:
        clock.tick(60)
        window.blit(GROUND_IMG, (ground_scroll,
                    WINDOW_HEIGHT-GROUND_IMG.get_height()))
        window.blit(BACKGROUND_IMG, (0, 0))
        player.draw(window)

        ground_scroll -= SCROLL_SPEED

        if abs(ground_scroll) > 50:
            ground_scroll = 0

        pygame.display.update()
        if started:
            player.move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    started = True
                    player.flap()


if __name__ == "__main__":
    main()
