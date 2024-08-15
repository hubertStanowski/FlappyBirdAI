from constants import *
from player import Player
from ground import Ground
from pipe import DoublePipeSet
from population import Population

import pygame


def main():
    pygame.init()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.display.set_caption("Flappy Bird NEAT AI")

    clock = pygame.time.Clock()
    ground = Ground()
    pipes = DoublePipeSet()
    h_player = Player()
    h_player.flying = False
    population = Population(size=40)
    # With small population it is likely that NEAT will have to be redone ("RESET" message), but with big population
    # it is likely that there will be no need for evolution due to how uncomplicated FlappyBird is
    # for evolution ~size=40 when fps=60

    human_playing = False
    fps = 60

    # temp = True
    # while temp:
    #     for event in pygame.event.get():
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_SPACE:
    #                 temp = False

    while True:
        clock.tick(fps)

        window.blit(BACKGROUND_IMG, (0, 0))

        if h_player.flying or not human_playing:
            pipes.update(h_player.hitbox.x)
        pipes.draw(window)

        if h_player.alive:
            ground.update()
        ground.draw(window)

        if human_playing:
            h_player.draw(window)
            h_player.update(ground, pipes)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        h_player.flap()

            score = h_player.score
        else:
            if not population.finished():
                population.update_survivors(window, ground, pipes)
            else:
                population.natural_selection()
                pipes = DoublePipeSet()
            # print(([player.score for player in population.players if player.alive]))

            if population.generation >= 5 and population.best_score == 0:
                # TODO cap no population improvement instaed of just score == 0
                # TODO keep track of prevoius gen score and if this gen after death doesn't have a better score increase population staleness -  reset after 5 times this occurs
                population = Population(len(population.players))
                pipes = DoublePipeSet()
                display_reset(window)

            score = population.gen_best_score
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            display_generation(window, population)
        display_score(window, score)

        pygame.display.update()


def display_generation(window, population: Population):
    current_generation = population.generation
    font = pygame.font.SysFont(FONT, GENERATION_FONT_SIZE)
    label = font.render(f"Gen: {current_generation}", True, BLACK)
    label_rect = label.get_rect(topleft=(10, 10))
    window.blit(label, label_rect)


def display_score(window, score):
    font = pygame.font.SysFont(FONT, SCORE_FONT_SIZE)
    label = font.render(str(score), True, BLACK)
    label_rect = label.get_rect(center=(WINDOW_WIDTH // 2, 30))

    window.blit(label, label_rect)


def display_reset(window):
    font = pygame.font.SysFont(FONT, RESET_FONT_SIZE)
    label = font.render("RESET", True, RED)
    label_rect = label.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 5))
    window.blit(label, label_rect)
    pygame.display.update()
    pygame.time.delay(1000)


if __name__ == "__main__":
    main()
