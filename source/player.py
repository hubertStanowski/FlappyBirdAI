from constants import *
from pipe import PipeSet
from ground import Ground
from genome import Genome

from collections import deque


class Player:
    def __init__(self, x, y) -> None:
        self.img = PLAYER_IMG
        self.hitbox = self.img.get_rect()
        self.hitbox.center = (x, y)
        self.vel = 0
        self.pipes = deque([PipeSet(), PipeSet(x_offset=PIPE_SEPERATION)])
        self.ground = Ground()
        self.alive = True
        self.on_ground = False
        self.flying = False
        self.score = 0
        # NEAT related
        self.fitness: int = 0
        self.generation = 0
        self.genome_inputs = 2      # TODO tune later
        self.genome_outputs = 1
        self.genome: Genome = Genome(self.genome_inputs, self.genome_outputs)

    def draw(self, window) -> None:
        for pipeset in self.pipes:
            pipeset.draw(window)

        self.ground.draw(window)

        self.display_score(window)

        if not self.flying:
            current_img = self.img
        elif self.vel < 10:
            current_img = pygame.transform.rotate(self.img, 30)
        else:
            angle = max(30 - (self.vel - 10) * 12, -90)
            current_img = pygame.transform.rotate(self.img, angle)

        window.blit(current_img, self.hitbox)

    def update(self):
        if self.on_ground or not self.flying:
            return

        self.vel += GRAVITY
        self.hitbox.y += self.vel

        self.check_collisions()

        change = False
        for pipeset in self.pipes:
            pipeset.update()
            if pipeset.check_passed(self):
                self.score += 1
                print(self.score)
            if pipeset.is_offscreen():
                change = True

        if change:
            self.pipes.popleft()
            self.pipes.append(PipeSet())

        self.ground.update()

    def flap(self):
        if self.alive:
            self.flying = True
            self.vel = -FLAP_SPEED

    def check_collisions(self):
        for pipeset in self.pipes:
            if pipeset.collides(self):
                self.alive = False

        self.on_ground = self.ground.collides(self)
        if self.on_ground:
            self.alive = False

        return self.alive

    def display_score(self, window):
        font = pygame.font.SysFont(FONT, SCORE_FONT_SIZE)
        score_label = font.render(str(self.score), True, WHITE)
        score_rect = score_label.get_rect(center=(WINDOW_WIDTH // 2, 30))

        window.blit(score_label, score_rect)
