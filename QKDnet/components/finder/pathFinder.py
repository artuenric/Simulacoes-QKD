from abc import ABC, abstractmethod
import networkx as nx

class PathFinder(ABC):
    """
    Busca as rotas para o controlador.
    """
    def __init__(self, name) -> None:
        self.name = name
    
    @abstractmethod
    def get_paths(self):
        pass
