from .sorter import Sorter

class ShortestRouteSorter(Sorter):
    def __init__(self):
        super().__init__()
        self.category = "Shortest Route"
    
    def sort(self, requests):
        """
        Ordena as requisições com base na rota mais curta.

        Args:
            requests (list): Lista de requisições a serem ordenadas.
        
        Returns:
            sorted_requests (list): Lista de requisições ordenadas.
        """
        sorted_requests = sorted(requests, key=lambda request: request.route_length)
        return sorted_requests