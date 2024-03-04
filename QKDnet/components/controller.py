import networkx as nx
from protocols import *
from finder import *
from itertools import islice

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
        self.current_requests = []
    
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
    
    def allocate(self):
        """
        Aloca as rotas de acordo com o tempo de atendimento para os pedidos e atualiza a lista de requisições.
        
        Args:
            requests (list): Lista de requests.
        """

         # Todos os links já utilizados
        all_used_links = set()
        # Links utilizados apenas por BB84 e B92
        bb84_b92_used_links = set()
        # Contador de rotas E91 (para que não haja muitos E91 com links compartilhados)
        e91_count = 0
        
        for r in self.requests:
            # Calcula as rotas de menor custo para a request
            routes = self.pathFinder.get_paths(r.alice, r.bob)
            
            # Itera sobre as rotas
            for route in routes:
                # Lista de pares de elementos adjacentes da lista route (canais)
                route_links = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
                # Checa se nenhum link dessa rota já foi usado em uma rota anterior
                
                # ISSO AQUI TEM QUE MUDAR DE ACORDO COM A CAPACIDADE DE CADA LINK
                if not any(link in all_used_links for link in route_links):
                    # Se a app for BB84 ou B92, adiciona os links usados no conjunto de links usados apenas por essas apps
                    if r.app == 'BB84' or r.app == 'B92':
                        bb84_b92_used_links.update(route_links)
                    # Adicionando as informações de rota, app e prioridade
                    r.route = route
                    self.current_requests.append(r)
                    # Adiciona os links usados no conjunto de links usados
                    all_used_links.update(route_links)
                    break
                elif r.app == 'E91':
                    # Se nenhum dos links desta rota está nos links utilizados pelos outros tipos de protocolo, os links que estão sendo utilizados são dos outros E91
                    if not any(e91_link in bb84_b92_used_links for e91_link in route_links):
                        # Para que não haja tantos E91 com links compartilhados, só 3 rotas E91 que compartilham links serão alocadas no máximo
                        if e91_count < self.network.neprs:
                            # Adicionando as informações de rota, app e prioridade
                            r.route = route
                            self.current_requests.append(r)
                            # Adicionando o link ao conjunto de links usados
                            all_used_links.update(route_links)
                            e91_count += 1
                        break
            
    
    def send_requests(self, requests):
        """
        Envia as requisições para a rede que as executa a partir da lista.
        
        Args:
            requests (list): Lista de requisições.
        """
        # Adiciona na "memória" do controlador uma cópia das requisições recebidas
        self.requests = requests.copy()
        # Estima o tempo para atendimento dos requests
        self.estimate_time(self.requests)
        # Ordena as requisições por tempo estimado
        self.requests = sorted(self.requests, key=lambda r: r.time_left) #Talvez seja necessário implementar um método de ordenação próprio por meio de uma classe
        
        # Enquanto houver requisições na lista de requisições
        while len(self.requests) > 0: # fnal do laço remover as requests de current_requests
            
            # Aloca as rotas de acordo com o tempo de atendimento e atualiza a lista de requisições atuais.
            self.allocate_routes(self.requests)
            
            for request in self.current_requests:
                # Executa a aplicação QKD
                request.protocol.run(self.network, request.route)
                # Atualiza o númerp de chaves obtidas
                request.update_keys(len(request.protocol.shared_key))
                # Atualiza a lista de requisições
                if request.keys_need <= 0:
                    self.current_requests.remove(request)
            
            # Coletando dados
            # CRIAR FORMA LEGAL DE COLETAR DADOS
            self.time += 1
   
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
            request.set_time_left(estimated_time)