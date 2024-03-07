import networkx as nx
from ..protocols import *
from .finder import *
from time import sleep
import logging as log
log.basicConfig(
    level=log.INFO,  # Nível mínimo de gravidade para registrar
    format='%(asctime)s - %(message)s'  # Formato da mensagem de log
)


class Controller():
    """
    Controlador SDN para a rede quântica.
    """
    def __init__(self, network) -> None:
        self.network = network
        self.pathFinder = None
        self.set_paths_calculation('shortest')
        self.received_requests = []
        self.requests = []
        self.current_requests = set()
        self.time = 0
    
    def set_paths_calculation(self, routes_calculation_type):
        """
        Define o tipo de cálculo de rotas que o controlador utilizará.

        Args:
            routes_calculation_type (str): shortest, kshortest, all, klength.
        """
        # Calcula as rotas de menor custo
        if routes_calculation_type == 'shortest':
            self.pathFinder = ShortestPaths(self.network)
        elif routes_calculation_type == 'kshortest': 
            self.pathFinder = KShortestPaths(self.network)
        elif routes_calculation_type == 'all':
            self.pathFinder = AllPaths(self.network)
        elif routes_calculation_type == 'klength':
            self.pathFinder = KLengthPaths(self.network)
    
    def set_network(self, network):
        """
        Define a rede que o controlador trabalha.  
        
        Args:
            network (Network): Rede em que o controlador atua.
        """
        self.network = network
        network.set_controller(self)
    
    def add_received_requests(self, requests):
        """
        Define as requisições recebidas pelo controlador.
        
        Args:
            requests (list): Lista de requisições.
        """
        self.received_requests.append(requests)
    
    def add_current_requests(self, requests):
        """
        Define as requisições atuais do controlador.
        
        Args:
            requests (list): Lista de requisições.
        """
        self.current_requests.append(requests)
    
    def calculate_shortest_route(self, alice, bob):
        """
        Procura a rota de menor custo.
        
        Args:
            alice, bob (node): Nós do grafo da rede.

        Returns:
            route (list): Lista de nós que compõem a rota.
        """
        route = []
        route.append(nx.shortest_path(self.network.G, alice, bob))
        
        return route
    
    def allocate(self, requests):
        """
        Aloca as rotas de acordo com o tempo de atendimento para os pedidos e atualiza a lista de requisições.
        
        Args:
            requests (list): Lista de requests.
        """
        
        # Lista de requisições a serem atendidas
        current_requests = []
        
        # Itera sobre as requisições
        for r in self.requests:
            # Calcula as rotas de menor custo para a request
            routes = self.pathFinder.get_paths(r.alice, r.bob)
            
            # Itera sobre as rotas
            for route in routes:
                # Lista de pares de elementos adjacentes da lista route (canais)
                route_links = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
                
                log.info(f"Capacidade da rota {route}: {list(self.network.channels[(link[0], link[1])]['capacity'] for link in route_links)}")
                
                # Se todos os links da rota tem capacidade maior que a carga atual, aloca a rota
                if all(self.network.channels[(link[0], link[1])]["capacity"] > self.network.channels[(link[0], link[1])]["load"] for link in route_links):
                    log.info(f"Rota {route} alocada para a requisição {r.num_id}.")
                    r.route = route
                    log.info(f"Adicionando request {r.num_id} na lista de requests atuais.")
                    current_requests.append(r)
                    log.info(f"Load da rota: {list(self.network.channels[(link[0], link[1])]["load"] for link in route_links)}")
                    self.network.add_load(route)
                    break
        
        return current_requests
            
    
    def send_requests(self, requests):
        """
        Envia as requisições para a rede que as executa a partir da lista.
        
        Args:
            requests (list): Lista de requisições.
        """
        
        log.debug(f"Requisições recebidas: {list(request.get_info() for request in requests)}")
        
        # Adiciona na "memória" do controlador uma cópia das requisições recebidas
        self.requests = requests.copy()
        # Estima o tempo para atendimento dos requests
        self.estimate_time(self.requests)
        # Ordena as requisições por tempo estimado
        received_requests = sorted(self.requests, key=lambda r: r.estimated_time) #Talvez seja necessário implementar um método de ordenação próprio por meio de uma classe    
        
        # Enquanto houver requisições na lista de requisições
        while len(self.requests) > 0: # fnal do laço remover as requests de current_requests
            # Aloca as rotas de acordo com o tempo de atendimento e atualiza a lista de requisições atuais.
            current_requests = self.allocate(received_requests)
            
            print("Requests sendo atendidas: ", list(request.num_id for request in current_requests))
            
            for request in current_requests:
                print(f"Request {request.num_id} sendo atendida.")
                # Executa a aplicação QKD
                request.protocol.run(self.network, request.route)
                # Atualiza o númerp de chaves obtidas
                request.update_keys(len(request.protocol.shared_key))
                print("Chaves Necessárias para finalizar a App:", request.keys_need)
                print("Chaves Obtidas:", len(request.protocol.shared_key))
                
                if request.keys_need <= 0:
                    print(f"Removendo request {request.num_id} da lista de requests.")
                    print(f"Requests: {list(request.num_id for request in self.requests)}")
                    self.requests.remove(request)
                    print("R E M O V I a request da lista de requests.", list(request.num_id for request in self.requests))
                    request.served = True
                
                elif request.current_time == request.max_time:
                    print("Request NÃO atendida.")
                    self.current_requests.remove(request)
                    request.served = False
            
                self.network.remove_load(request.route)
            #sleep(2)
            # Atualiza o tempo de atendimento
            #self.update_time()
   
    def estimate_time(self, requests):
        """
        Estima o tempo de atendimento para as requisições.

        Args:
            requests (list): Lista de requisições.
        """

        for request in requests:
            # Calcula o tempo estimado de atendimento
            estimated_time = 1 + ((request.keys_need)/self.network.nqubits) * request.protocol.sucess_rate
            # Atualiza o tempo estimado de atendimento
            request.set_estimated_time(estimated_time)
    
    def update_time(self):
        """
        Atualiza o tempo de atendimento para as requisições e do controlador.
        """
        self.time += 1
        for request in self.requests:
            request.current_time += 1