from .pathFinder import *

class ShortestPath(PathFinder):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Shortest path"
        
    def get_paths(self, alice, bob):
        """
        Procura a rota de menor custo.
        
        Args:
            alice, bob (node): Nós do grafo da rede.

        Returns:
            route (list): Lista de nós que compõem a rota.
        """
        route = []
        route.append(nx.shortest_path(self.network.G, alice, bob))
        
        return route