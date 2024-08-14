from constants import *
from player import Player
from population import Population

import pygame


def main():
    pygame.init()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.display.set_caption("Flappy Bird AI")

    clock = pygame.time.Clock()
    player = Player()
    population = Population(size=1000)

    human_playing = False

    while True:
        clock.tick(60)

        window.blit(BACKGROUND_IMG, (0, 0))

        if human_playing:
            player.draw(window)

            player.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.flying = True
                        player.flap()
        else:
            if not population.finished():
                population.update_survivors(window, draw_best=True)
            else:
                population.natural_selection()
                print(population.generation)
            print(population.gen_best_score)

            # print(population.best_score)
            # print(len(population.species))

            # print(len(population.innovation_history))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

        pygame.display.update()


if __name__ == "__main__":
    main()
