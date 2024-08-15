from constants import *
from pipe import DoublePipeSet
from ground import Ground
from genome import Genome
from neat_config import NeatConfig


class Player:
    def __init__(self) -> None:
        self.img = PLAYER_IMG
        self.hitbox = self.img.get_rect()
        self.hitbox.center = (PLAYER_X, PLAYER_Y)
        self.vel = 0
        self.alive = True
        self.on_ground = False
        self.flying = True
        self.score = 0
        # NEAT related
        self.fitness: int = 0
        self.lifespan = 0
        self.best_score = 0
        self.generation = 0
        self.genome_inputs = 4
        self.genome_outputs = 1
        self.genome: Genome = Genome(self.genome_inputs, self.genome_outputs)
        self.vision = []

    def draw(self, window) -> None:

        if not self.flying and self.alive:
            current_img = self.img
        elif self.vel < 10:
            current_img = pygame.transform.rotate(self.img, 30)
        else:
            angle = max(30 - (self.vel - 10) * 12, -90)
            current_img = pygame.transform.rotate(self.img, angle)

        # collision_hitbox = self.hitbox.copy()
        # collision_hitbox.y += 10
        # collision_hitbox.x += 5
        # pygame.draw.rect(window, (255, 0, 0), collision_hitbox, 1)

        window.blit(current_img, self.hitbox)

    def update(self, ground: Ground, pipes: DoublePipeSet) -> None:
        if self.on_ground or not self.flying:
            return

        self.vel = min(self.vel + GRAVITY, FLAP_SPEED*2)
        self.hitbox.y += self.vel
        self.check_collisions(ground, pipes)

        if self.alive:
            self.lifespan += 1
            self.score = pipes.score

    def flap(self) -> None:
        if self.alive:
            self.flying = True
            self.vel = -FLAP_SPEED

    def check_collisions(self, ground: Ground, pipes: DoublePipeSet) -> bool:
        for pipeset in pipes.pipesets:
            if pipeset.collides(self):
                self.alive = False

        self.on_ground = ground.collides(self)
        if self.on_ground:
            self.alive = False
            self.flying = False

        return self.alive


# NEAT

    def clone(self) -> 'Player':
        clone = Player()
        clone.genome = self.genome.clone()
        clone.fitness = self.fitness
        clone.generation = self.generation
        clone.best_score = self.score
        clone.genome.generate_network()

        return clone

    def crossover(self, config: NeatConfig, other_parent: 'Player') -> 'Player':
        child = Player()
        child.genome = self.genome.crossover(config, other_parent.genome)
        child.genome.generate_network()

        return child

    # TODO tune later
    def update_fitness(self) -> None:
        self.fitness = 1 + self.score**2 + self.lifespan / 10

    def remap(self, value, start1, stop1, start2, stop2) -> float:
        """
            Remaps a value in range(start1, stop1) proportionately to range(start2, stop2) and returns it
        """
        return (value - start1) / (stop1 - start1) * (stop2 - start2) + start2

    def look(self, ground: Ground, pipes: DoublePipeSet) -> None:
        self.vision = []
        closest_pipeset = pipes.pipesets[0] if not pipes.pipesets[0].passed else pipes.pipesets[1]
        height_cap = WINDOW_HEIGHT-ground.hitbox.height - self.hitbox.height

        self.vision.append(self.remap(
            self.vel, -FLAP_SPEED, 2*FLAP_SPEED, -1, 1))
        self.vision.append(self.remap(
            closest_pipeset.top.hitbox.x - self.hitbox.x, 0, WINDOW_WIDTH-self.hitbox.x, 1, 0))
        self.vision.append(self.remap(
            max(0, closest_pipeset.bottom.hitbox.top - self.hitbox.y), 0, height_cap, 0, 1))
        self.vision.append(self.remap(
            max(0, self.hitbox.y - closest_pipeset.top.hitbox.bottom), 0, height_cap, 0, 1))

        # print(self.vision)

    def decide(self) -> None:
        """
        ! Only use after look() !
        """
        decision = self.genome.feed_forward(self.vision)[0]
        # print(decision)

        if decision > 0.6:
            self.flap()
