from .pathFinder import *
from itertools import islice

class KShortestPaths(PathFinder):
    def __init__(self, network) -> None:
        super().__init__()
        self.name = "K shortest paths"
        self.network = network
        self.k = 5
        
    def get_paths(self, alice, bob):
        """
        Procura k rotas de menor custo. Para o caso de redes do tipo malha, é mais efetivo que `calculate_shortest_routes()`, já que esta retorna apenas as rotas do canal direto alice-bob.
        Args:
            alice, bob (node): Nós do grafo da rede.

        Returns:
            route (list): Lista com k listas de nós que compõem a rota
        """
        return list(islice(nx.shortest_simple_paths(self.network.G, alice, bob, weight=None), self.k ))