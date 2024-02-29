from .pathFinder import *

class KLengthPaths(PathFinder):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Paths of K length"
    
    def dfs_paths(self, source, target, length, path=None):
        """
        Realiza uma busca em profundidade (DFS) em busca de caminhos de um comprimento específico entre dois nós.

        Args:
            source (node): Nó de origem.
            target (node): Nó de destino.
            length (int): Comprimento desejado do caminho.
            path (list, optional): Caminho parcial atual. Defaults to None.

        Return:
            list: Lista de nós que compõem um caminho de comprimento específico entre source e target.
        """
        G = self.network.G
         # Inicializa o caminho se não estiver definido
        if path is None:
            path = [source]
        # Verifica se o comprimento do caminho atingiu o objetivo
        if len(path) == length:
            if path[-1] == target:
                yield path
            return
        # Explora os vizinhos do nó de origem
        for neighbor in G.neighbors(source):
            # Garante que o vizinho não esteja no caminho atual
            if neighbor not in path:
                # Recursivamente busca caminhos a partir do vizinho
                yield from self.dfs_paths(neighbor, target, length, path + [neighbor])
    
    def get_paths(self, alice, bob, length):
        """
        Encontra todos os caminhos de um comprimento específico entre dois nós.

        Args:
            alice (node): Nó de origem.
            bob (node): Nó de destino.
            length (int): Comprimento desejado do caminho.

        Returns:
            list: Lista de caminhos entre source e target com o comprimento especificado.
        """
         # Chama a função de busca em profundidade com comprimento + 1 porque length inclui o nó de origem
        return list(self.dfs_paths(alice, bob, length + 1))