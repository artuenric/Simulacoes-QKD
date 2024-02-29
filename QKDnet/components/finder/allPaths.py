from .pathFinder import *

class AllPaths(PathFinder):
    def __init__(self) -> None:
        super().__init__()
        self.name = "All paths"
        
    def get_paths(self, alice, bob):
        """
        Procura a todas as rotas.
        
        Args:
            alice, bob (node): Nós do grafo da rede.

        Returns:
            route (list): Lista de listas de nós que compõem a rota.
        """
        return sorted(list(nx.all_simple_paths(self.network.G, alice, bob)), key=len)