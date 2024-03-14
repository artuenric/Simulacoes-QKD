from .sorter import Sorter

class FifoSorter(Sorter):
    def __init__(self):
        super().__init__()
        self.category = "FIFO"

    def sort(self, requests):
        """
        Ordena as requisições com base na ordem de chegada.

        Args:
            requests (list): Lista de requisições a serem ordenadas.
        
        Returns:
            requests (list): Lista de requisições ordenadas.
        """
        return requests