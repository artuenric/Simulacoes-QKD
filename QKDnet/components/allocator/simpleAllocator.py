from ...utils import Logger
from .allocator import Allocator

class SimpleAllocator(Allocator):
    def __init__(self, controller) -> None:
        super().__init__(controller)
        self.controller = controller
        self.category = 'Simple'
        
    def allocate(self):
        """
        Aloca uma rota para cada request de acordo com o tempo de atendimento para os pedidos e atualiza a lista de requisições.
        
        Args:
            requests (list): Lista de requests.
        """
        
        # Itera sobre as requisições
        for r in self.controller.requests.copy():
            
            # Se a requisição expirou, remove da lista de requisições
            if r.time_left == 0:
                Logger.get_instance().log(f"Request: {r.num_id} - Expirou!")
                r.finished = True
                self.controller.data_base.collect_failed_requests_data(r)
                self.controller.requests.remove(r)
                continue
            
            # Calcula as rotas de menor custo para a request
            routes = self.controller.path_finder.get_paths(r.alice, r.bob)
            
            Logger.get_instance().log(f"Request: {r.num_id} - Rotas: {routes}")
            
            # Itera sobre as rotas
            for route in routes:
                # Lista de pares de elementos adjacentes da lista route (canais)
                route_links = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
                
                Logger.get_instance().log(f"Capacidade da rota {route}: {list(self.controller.network.channels[(link[0], link[1])]['capacity'] for link in route_links)}.")
                Logger.get_instance().log(f"Load da rota {route}: {list(self.controller.network.channels[(link[0], link[1])]['load'] for link in route_links)}.")
                
                # Se todos os links da rota tem capacidade maior que a carga atual, aloca a rota
                if all(self.controller.network.channels[(link[0], link[1])]["capacity"] > self.controller.network.channels[(link[0], link[1])]["load"] for link in route_links):
                    r.route = route
                    Logger.get_instance().log(f"Request: {r.num_id} - Rota {route}.")
                    
                    self.controller.current_requests.append(r)
                    Logger.get_instance().log(f"Request: {r.num_id} - Adicionado requests na lista de requests atuais.")
                    
                    self.controller.network.add_load(route)
                    Logger.get_instance().log(f"Add Load na rota: {list(self.controller.network.channels[(link[0], link[1])]["load"] for link in route_links)}")
                    break
        
        Logger.get_instance().log(f"Requests escolhidas para alocação: {list(request.num_id for request in self.controller.current_requests)}")