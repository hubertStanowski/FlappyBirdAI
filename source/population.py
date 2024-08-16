from neat_config import NeatConfig
from innovation_history import InnovationHistory
from player import Player
from species import Species
from ground import Ground
from pipe import DoublePipeSet

import math


class Population:
    def __init__(self, config: NeatConfig, size: int) -> None:
        self.config: NeatConfig = config
        self.size = size
        self.innovation_history: list[InnovationHistory] = []
        self.players: list[Player] = []
        self.best_player: Player | None = None
        self.best_score: int = 0
        self.gen_players: list[Player] = []
        self.gen_best_score: int = 0
        self.prev_gen_best_score: int = 0
        self.generation: int = 1
        self.species: list[Species] = []
        self.staleness = 0

        for i in range(size):
            self.players.append(Player())
            self.players[-1].genome.mutate(self.config,
                                           self.innovation_history)
            self.players[-1].genome.generate_network()

    def finished(self) -> bool:
        for player in self.players:
            if player.alive or (player.flying and self.config.show_dying):
                return False
        return True

    def update_survivors(self, window, ground: Ground, pipes: DoublePipeSet) -> None:
        for player in self.players:
            if player.alive:
                player.look(ground, pipes)
                player.decide()

            if (player.flying and self.config.show_dying) or player.alive:
                player.draw(window, sensor_view=self.config.sensor_view)
                player.update(ground, pipes)

            if player.score > self.gen_best_score:
                self.gen_best_score = player.score

    def natural_selection(self) -> None:
        if self.prev_gen_best_score >= self.gen_best_score:
            self.staleness += 1
        else:
            self.staleness = 0
        self.prev_gen_best_score = self.gen_best_score
        # print(self.staleness)

        prev_best = self.players[0]
        self.speciate()
        self.update_fitness()
        self.sort()
        self.remove_low_performers_from_species()
        self.update_best_player()
        self.kill_low_performing_species()
        self.kill_stale_species()

        average_fitness_sum = self.get_avg_fitness_sum()
        children = []
        for s in self.species:
            children.append(s.best_player.clone())
            children_count = math.floor((s.average_fitness /
                                         average_fitness_sum * len(self.players)) - 1)

            for i in range(children_count):
                children.append(s.reproduce(
                    self.config, self.innovation_history))

        if len(children) < len(self.players):
            children.append(prev_best.clone())

        while len(children) < len(self.players):
            children.append(self.species[0].reproduce(
                self.config, self.innovation_history))

        self.players = children.copy()
        self.generation += 1
        for player in self.players:
            player.genome.generate_network()

    def speciate(self) -> None:
        for s in self.species:
            s.players = []

        for player in self.players:
            assigned = False
            for s in self.species:
                if s.is_this_species(player.genome):
                    s.add(player)
                    assigned = True
                    break
            if not assigned:
                self.species.append(Species(player))

    def sort(self) -> None:
        for s in self.species:
            s.sort()

        self.species.sort(key=lambda s: s.best_fitness, reverse=True)

    def kill_low_performing_species(self) -> None:
        average_fitness_sum = self.get_avg_fitness_sum()
        kill_list = []

        for i in range(len(self.species)):
            if (self.species[i].average_fitness / average_fitness_sum * len(self.players)) < 1:
                kill_list.append(i)

        for i in kill_list:
            self.species.pop(i)

    def kill_stale_species(self) -> None:
        kill_list = []
        # starting at idx 2 so that we have at least two species (better 2 stale ones than just having 1 or 0)
        for i in range(2, len(self.species)):
            if self.species[i].staleness >= self.config.get_species_staleness_limit():
                kill_list.append(i)

        for i in kill_list:
            self.species.pop(i)

    def update_fitness(self) -> None:
        for player in self.players:
            player.update_fitness()

    def get_current_best(self) -> Player:
        """
        !ONLY USE AFTER SORTING!
        """
        # best player is the one with the highest fitness while being alive
        for player in self.players:
            if player.alive:
                return player

        # if every player is dead just return the one with the highest fitness
        return self.players[0]

    def update_best_player(self) -> None:
        current_best = self.species[0].players[0]
        current_best.generation = self.generation

        if current_best.score >= self.best_score:
            self.best_score = current_best.score
            self.best_player = current_best.clone()
            self.gen_players.append(current_best.clone())

        self.gen_best_score = 0

    def get_avg_fitness_sum(self) -> float:
        return sum(species.average_fitness for species in self.species)

    def remove_low_performers_from_species(self) -> None:
        for species in self.species:
            species.remove_low_performers()
            species.share_fitness()
            species.update_average_fitness()
