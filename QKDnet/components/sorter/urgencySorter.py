from .sorter import Sorter

def custom_sort(request):
    """
    Ordena as requisições de acordo com a urgência que é definida pelas métricas do return, com prioridade nessa ordem.

    Args:
        request (Request): Requisição a ser ordenada.

    Returns:
        tuple: Métricas de urgência da requisição.
    """
    return (
        request.max_start_time,
        request.estimated_time,
        request.max_time,
        request.route_length
    )
        
class UrgencySorter(Sorter):
    def __init__(self):
        super().__init__()
        self.category = "Urgency"
    
    def sort(self, requests):
        """
        Ordena as requisições com base na urgência.

        Args:
            requests (list): Lista de requisições a serem ordenadas.
        
        Returns:
            sorted_requests (list): Lista de requisições ordenadas.
        """
        sorted_requests = sorted(requests, key=custom_sort)
        return sorted_requests