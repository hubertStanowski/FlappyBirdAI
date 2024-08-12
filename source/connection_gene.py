from node_gene import NodeGene


class ConnectionGene:
    def __init__(self, input: NodeGene, output: NodeGene, weight: float, innovation_number: int, enable: bool = True) -> None:
        self.input: NodeGene = input
        self.output: NodeGene = output
        self.weight: float = weight
        self.innovation_number: int = innovation_number
        self.enable: bool = enable
