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
        request.max_start_time, # Menor tempo máximo para o início do atendimento
        - request.estimated_time, # Maior tempo estimado para ser atendido
        - request.max_time, # Maior tempo máximo de request
        request.route_length # Menor rota
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
        
        # Ordena as requisições
        sorted_requests = sorted(requests, key=custom_sort)
        
        return sorted_requests