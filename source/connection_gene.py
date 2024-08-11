from node_gene import NodeGene


class ConnectionGene:
    def __init__(self) -> None:
        self.in_node: NodeGene = None
        self.out_node: NodeGene = None
        self.weight: float = 0.0
        self.enable: bool = True
        self.innovation_number: int = 0
