from neat_config import NeatConfig
from innovation_history import InnovationHistory
from player import Player
from species import Species


class Population:
    def __init__(self, size: int) -> None:
        self.config: NeatConfig = NeatConfig()
        self.innovation_history: list[InnovationHistory] = []
        self.players: list[Player] = []
        self.best_player: Player | None = None
        self.best_score: int = 0
        self.gen_players: list[Player] = []
        self.gen_best_score: int = 0
        self.generation: int = 1
        self.species: list[Species] = []

        for i in range(size):
            self.players.append(Player())
            self.players[-1].genome.mutate(self.config,
                                           self.innovation_history)
            # self.players[-1].genome.generate_network()    # TODO probably sooonsih

    def natural_selection(self) -> None:
        pass

    def speciate(self) -> None:
        pass

    def sort(self):
        for s in self.species:
            s.sort()

        self.species.sort(key=lambda s: s.best_fitness, reverse=True)

    def kill_low_performing_species(self) -> None:
        pass

    def kill_stale_species(self) -> None:
        pass

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

    def get_avg_fitness_sum(self) -> float:
        return sum(species.average_fitness for species in self.species)

    def remove_low_performers(self) -> None:
        for species in self.species:
            species.remove_low_performers()
            species.share_fitness()
            species.update_average_fitness()
