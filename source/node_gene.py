
import math

# TODO ? specify layer when initializing ?


class NodeGene:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.layer: int = 0
        self.output_connections = []
        self.input_sum: float = 0
        self.output_value: float = 0

    def is_connected_to(self, other: 'NodeGene') -> bool:
        if other.layer < self.layer:
            for i in range(len(other.output_connections)):
                if other.output_connections[i].output == self:
                    return True
        elif other.layer > self.layer:
            for i in range(len(self.output_connections)):
                if self.output_connections[i].output == other:
                    return True

        return False

    def sigmoid(self, x) -> float:
        # Modified formula from creators of NEAT
        return 1.0 / (1.0 + math.exp(-4.9 * x))

    def engage(self) -> None:
        if self.layer != 0:
            self.output_value = self.sigmoid(self.input_sum)

        for current_connection in self.output_connections:
            if current_connection.enabled:
                current_connection.output.input_sum += current_connection.weight * self.output_value

    def clone(self) -> 'NodeGene':
        clone = NodeGene(self.id)
        clone.layer = self.layer

        return clone
