from node_gene import NodeGene
from genome import Genome


class InnovationHistory:
    def __init__(self) -> None:
        self.data = []
        self.next_innovation_number = 1


class InnovationHistoryNode:
    def __init__(self, input: int, output: int, innovation_number: int, connected_innovation_numbers: list[int]) -> None:
        self.input: NodeGene = input
        self.output: NodeGene = output
        self.innovation_number: int = innovation_number
        self.connected_innovation_numbers: list[int] = connected_innovation_numbers.copy(
        )  # idk why autopep8 does this

    def matches(self, genome: Genome, input: NodeGene, output: NodeGene):
        if len(genome.connections) != len(self.connected_innovation_numbers):
            return False
        if input.id != self.input or output.id != self.output:
            return False

        for i in range(len(genome.connections)):
            if not genome.connections[i].innovation_number in self.connected_innovation_numbers:
                return False

        return True
