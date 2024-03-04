from .pathFinder import *

class ShortestPaths(PathFinder):
    def __init__(self, network) -> None:
        super().__init__()
        self.name = "Shortest paths"
        self.network = network
        
    def get_paths(self, alice, bob):
        """
        Procura as rotas de menores custos.
        
        Args:
            alice, bob (node): Nós do grafo da rede.

        Returns:
            route (list): Lista de nós que compõem a rota.
        """
        return list(nx.all_shortest_paths(self.network.G, alice, bob))
    