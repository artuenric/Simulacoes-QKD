from .sorter import Sorter

class LongestRouteSorter(Sorter):
    def __init__(self):
        super().__init__()
        self.category = "Longest Route"
    
    def sort(self, requests):
        """
        Ordena as requisições com base na rota mais longa.

        Args:
            requests (list): Lista de requisições a serem ordenadas.
        
        Returns:
            sorted_requests (list): Lista de requisições ordenadas.
        """
        sorted_requests = sorted(requests, key=lambda request: request.route_length, reverse=True)
        return sorted_requests