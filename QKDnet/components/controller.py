from ..protocols import *
from ..utils import Logger
from .finder import *
from .sorter import *
from .allocator import *
from .data import DataBase

import networkx as nx

class Controller():
    """
    Controlador SDN para a rede quântica.
    """
    def __init__(self, network) -> None:
        # Elementos do controlador
        self.network = network
        self.path_finder = None
        self.sorter = None
        self.allocator = None
        # Definindo os tipos dos elementos
        self.set_sorter('urgency')
        self.set_path_finder('kshortest')
        self.set_allocator('simple')
        self.data_base = DataBase()
        # Dados
        self.received_requests = []
        self.requests = []
        self.current_requests = []
        self.time = 0
    
    def set_path_finder(self, routes_calculation_type):
        """
        Define o tipo de cálculo de rotas que o controlador utilizará.

        Args:
            routes_calculation_type (str): Tipo de cálculo (shortest, kshortest, all, klength.)
        """
        # Calcula as rotas de menor custo
        if routes_calculation_type == 'shortest':
            self.path_finder = ShortestPaths(self.network)
        elif routes_calculation_type == 'kshortest': 
            self.path_finder = KShortestPaths(self.network)
        elif routes_calculation_type == 'all':
            self.path_finder = AllPaths(self.network)
        elif routes_calculation_type == 'klength':
            self.path_finder = KLengthPaths(self.network)
    
    def set_sorter(self, sorter_type):
        """
        Define o tipo de ordenação que o controlador utilizará.

        Args:
            sorter (str): Tipo de ordenação.
        """
        sorter_type = sorter_type.lower()
        
        if sorter_type == 'fifo':
            self.sorter = FifoSorter()
        elif sorter_type == 'urgency':
            self.sorter = UrgencySorter()
        elif sorter_type == 'shortest':
            self.sorter = ShortestRouteSorter()
        elif sorter_type == 'longest':
            self.sorter = LongestRouteSorter()
    
    def set_allocator(self, allocator):
        """
        Define o tipo de alocador das rotas.

        Args:
            allocator (str): Tipo de alocador.
        """
        if allocator == "simple":
            self.allocator = SimpleAllocator(self)
        
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

        # Estima o tempo para atendimento dos requests e define as rotas
        self.prepare_requests(self.requests)
        
        # Ordena as requisições
        self.requests = self.sorter.sort(self.requests)

        Logger.get_instance().log(f"Requisições ordenadas: {list(request.num_id for request in self.requests)}")


    def send_requests(self):
        """
        Envia as requisições para a rede que as executa a partir da lista.
        
        Args:
            requests (list): Lista de requisições.
        """
        
        # Enquanto houver requisições na lista de requisições
        while not all(request.finished for request in self.requests): # fnal do laço remover as requests de current_requests
            # Aloca as rotas de acordo com o tempo de atendimento e atualiza a lista de requisições atuais.
            self.allocator.allocate()

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
        
        # Coleta o tempo final
        self.data_base.final_time = self.time


    def prepare_requests(self, requests):
        """
        Estima o tempo de atendimento para as requisições e define a rota para ela.

        Args:
            requests (list): Lista de requisições.
        """

        for r in requests:
            # Calcula o tempo estimado de atendimento
            estimated_time = 1 + r.keys_need / (self.network.nqubits * r.protocol.sucess_rate)
            # Atualiza o tempo estimado de atendimento
            r.set_times(estimated_time)
            # Define a rotas para a requisição
            r.set_route(self.path_finder.get_paths(r.alice, r.bob))
    
    def update_time(self):
        """
        Atualiza o tempo de atendimento para as requisições e do controlador.
        """
        self.time += 1
        for request in self.requests:
            request.update_time()