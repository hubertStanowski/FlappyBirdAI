class NeatConfig:
    def __init__(self) -> None:
        self.next_innovation_number: int = 1
        self.weight_mutation_probablility = 0.8
        self.add_connection_mutation_probability = 0.05
        self.add_node_mutation_probablility = 0.01
        self.big_weight_mutation_probablility = 0.1
        self.crossover_connection_disable_probablility = 0.75
        self.no_crossover_probability = 0.25
        self.species_staleness_limit = 3
        self.population_staleness_limt = 10
        # compatibility coefficients: c1, c2, c3 and compatibility threshold (experimental values from article by creators of NEAT for not large population)
        self.excess_disjoint_coefficient: float = 1        # c1 = c2
        self.weight_difference_coefficient: float = 0.4    # c3
        self.compatibility_threshold: float = 3

        # View settings
        self.sensor_view = False
        self.show_dying = False
        self.draw_limit = 100

    def get_next_innovation_number(self) -> int:
        return self.get_next_innovation_number

    def update_next_innovation_number(self) -> int:
        self.next_innovation_number += 1

    def get_weight_mutation_probablility(self) -> float:
        return self.weight_mutation_probablility

    def get_add_connection_mutation_probability(self) -> float:
        return self.add_connection_mutation_probability

    def get_add_node_mutation_probablility(self) -> float:
        return self.add_node_mutation_probablility

    def get_big_weight_mutation_probablility(self) -> float:
        return self.big_weight_mutation_probablility

    def get_crossover_connection_disable_probablility(self) -> float:
        return self.crossover_connection_disable_probablility

    def get_no_crossover_probability(self) -> float:
        return self.no_crossover_probability

    def get_species_staleness_limit(self) -> int:
        return self.species_staleness_limit

    def get_population_staleness_limt(self) -> int:
        return self.population_staleness_limt

    def get_excess_disjoint_coefficient(self) -> float:
        return self.excess_disjoint_coefficient

    def get_weight_difference_coefficient(self) -> float:
        return self.weight_difference_coefficient

    def get_compatibility_threshold(self) -> float:
        return self.compatibility_threshold

    # View functions
    def toggle_sensor_view(self) -> None:
        self.sensor_view = not self.sensor_view

    def toggle_show_dying(self) -> None:
        self.show_dying = not self.show_dying

    def get_draw_limit(self) -> int:
        return self.draw_limit
