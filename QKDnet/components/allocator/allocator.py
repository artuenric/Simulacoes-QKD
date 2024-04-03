from abc import ABC, abstractmethod
class Allocator(ABC):
    """
    Aloca as rotas para o controlador.
    """
    def __init__(self, controller) -> None:
        self.controller = controller
        self.category = None
        
    @abstractmethod
    def allocate(self, **kwargs):
        pass
    
    