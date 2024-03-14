from ..protocols import *
from ..utils import Logger
from .finder import *
from .data import DataBase

import networkx as nx

class Controller():
    """
    Controlador SDN para a rede quântica.
    """
    def __init__(self, network) -> None:
        self.network = network
        self.pathFinder = None
        self.sorter = None
        self.data_base = DataBase()
        self.set_paths_calculation('kshortest')
        self.received_requests = []
        self.requests = []
        self.current_requests = []
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
        self.requests = requests
    
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
    
    def allocate(self):
        """
        Aloca as rotas de acordo com o tempo de atendimento para os pedidos e atualiza a lista de requisições.
        
        Args:
            requests (list): Lista de requests.
        """
        
        # Itera sobre as requisições
        for r in self.requests.copy():
            
            # Se a requisição expirou, remove da lista de requisições
            if r.time_left == 0:
                Logger.get_instance().log(f"Request: {r.num_id} - Expirou!")
                r.finished = True
                self.data_base.collect_failed_requests_data(r)
                self.requests.remove(r)
                continue
            
            # Calcula as rotas de menor custo para a request
            routes = self.pathFinder.get_paths(r.alice, r.bob)
            
            Logger.get_instance().log(f"Request: {r.num_id} - Rotas: {routes}")
            
            # Itera sobre as rotas
            for route in routes:
                # Lista de pares de elementos adjacentes da lista route (canais)
                route_links = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
                
                Logger.get_instance().log(f"Capacidade da rota {route}: {list(self.network.channels[(link[0], link[1])]['capacity'] for link in route_links)}.")
                Logger.get_instance().log(f"Load da rota {route}: {list(self.network.channels[(link[0], link[1])]['load'] for link in route_links)}.")
                
                # Se todos os links da rota tem capacidade maior que a carga atual, aloca a rota
                if all(self.network.channels[(link[0], link[1])]["capacity"] > self.network.channels[(link[0], link[1])]["load"] for link in route_links):
                    r.route = route
                    Logger.get_instance().log(f"Request: {r.num_id} - Rota {route}.")
                    
                    self.current_requests.append(r)
                    Logger.get_instance().log(f"Request: {r.num_id} - Adicionado requests na lista de requests atuais.")
                    
                    self.network.add_load(route)
                    Logger.get_instance().log(f"Add Load na rota: {list(self.network.channels[(link[0], link[1])]["load"] for link in route_links)}")
                    break
        
        Logger.get_instance().log(f"Requests escolhidas para alocação: {list(request.num_id for request in self.current_requests)}")
        
    
    def receive_requests(self, requests):
        """
        Recebe as requisições e as envia para a rede.
        
        Args:
            requests (list): Lista de requisições.
        """
        
        # Adiciona as requisições recebidas na lista de requisições
        self.received_requests = requests
        self.requests.extend(requests)
        self.data_base.collect_all_requests_data(requests)
        
        Logger.get_instance().log(f"Requisições recebidas pelo Controlador: {list(request.get_info() for request in requests)}")

        # Estima o tempo para atendimento dos requests
        self.estimate_time(self.requests)

        # Ordena as requisições
        self.requests = sorted(self.requests, key=lambda r: r.priority) #Talvez seja necessário implementar um método de ordenação próprio por meio de uma classe

        Logger.get_instance().log(f"Requisições ordenadas por tempo estimado: {list((request.num_id, request.estimated_time) for request in self.requests)}")


    def send_requests(self):
        """
        Envia as requisições para a rede que as executa a partir da lista.
        
        Args:
            requests (list): Lista de requisições.
        """
        
        # Enquanto houver requisições na lista de requisições
        while not all(request.finished for request in self.requests): # fnal do laço remover as requests de current_requests
            # Aloca as rotas de acordo com o tempo de atendimento e atualiza a lista de requisições atuais.
            self.allocate()

            Logger.get_instance().log(f"Requests sendo atendidas: {list(request.num_id for request in self.current_requests)}")

            for request in self.current_requests:
                Logger.get_instance().log(f"Request: {request.num_id} - Executando.")

                # Executa a aplicação QKD
                request.protocol.run(self.network, request.route)
                # Atualiza o númerp de chaves obtidas
                request.update_keys(len(request.protocol.shared_key))

                # Coleta de dados
                self.data_base.collect_protocol_data(request.protocol)
                
                Logger.get_instance().log(f"Request: {request.num_id} - Chaves Obtidas: {len(request.protocol.shared_key)}")
                Logger.get_instance().log(f"Request: {request.num_id} - Chaves necessárias: {request.keys_need}")

                if request.keys_need <= 0:
                    Logger.get_instance().log(f"Request: {request.num_id} - Atendida com sucesso.")
                    request.served = True
                    self.data_base.collect_served_requests_data(request)
                    request.finished = True
                    self.requests.remove(request)
                    Logger.get_instance().log(f"Request: {request.num_id} - Removida da lista de requests.")

                # "Limpa" a rota da requisição    
                self.network.remove_load(request.route)

            # Limpa a lista de requisições atuais
            self.current_requests.clear()

            # Atualiza o tempo de atendimento
            self.update_time()
            Logger.get_instance().log(f"Tempo atual: {self.time}")


    def estimate_time(self, requests):
        """
        Estima o tempo de atendimento para as requisições.

        Args:
            requests (list): Lista de requisições.
        """

        for r in requests:
            # Calcula o tempo estimado de atendimento
            estimated_time = 1 + r.keys_need / (self.network.nqubits * r.protocol.sucess_rate)
            # Atualiza o tempo estimado de atendimento
            r.set_estimated_time(estimated_time)
    
    def update_time(self):
        """
        Atualiza o tempo de atendimento para as requisições e do controlador.
        """
        self.time += 1
        for request in self.requests:
            request.update_time()