from connection_gene import ConnectionGene


class NodeGene:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.layer: int = 0
        self.output_connections: list[ConnectionGene] = []

    def is_connected_to(self, other: 'NodeGene') -> bool:
        if other.layer < self.layer:
            for i in range(len(other.output_connections)):
                if other.output_connections[i].out_node == self:
                    return True
        elif other.layer > self.layer:
            for i in range(len(self.output_connections)):
                if self.output_connections[i].out_node == other:
                    return True

        return False
