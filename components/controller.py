import networkx as nx
from components.protocols import *
from itertools import islice
class Controller():
    """
    Um objeto que atua como Controlador SDN para a rede quântica.
    """
    def __init__(self) -> None:
        self.network = None
    
    def set_network(self, network):
        """
        Define a rede que o controlador trabalha.  
        
        Args:
            network (Network): Rede em que o controlador atua.
        """
        self.network = network
        network.set_controller(self)
    
    def calculate_route(self, alice, bob):
        """
        Procura a rota de menor custo.
        Args:
            alice, bob (node): Nós do grafo da rede.

        Returns:
            route (list): Lista de nós que compõem a rota.
        """
        route = nx.shortest_path(self.network.G, alice, bob)
        return route
    
    def calculate_all_routes(self, alice, bob):
        """
        Procura as rotas de menor custo.
        Args:
            alice, bob (node): Nós do grafo da rede.

        Returns:
            route (list): Lista com listas de nós que compõem a rota.
        """
        return sorted(list(nx.all_simple_paths(self.network.G, alice, bob)), key=len)
    
    def calculate_k_shortest_routes(self, alice, bob, k=5):
        """
        Procura k rotas de menor custo. Para o caso de redes do tipo malha, é mais efetivo que `calculate_shortest_routes()`, já que esta retorna apenas as rotas do canal direto alice-bob.
        Args:
            alice, bob (node): Nós do grafo da rede.

        Returns:
            route (list): Lista com k listas de nós que compõem a rota
        """
        return list(islice(nx.shortest_simple_paths(self.network.G, alice, bob, weight=None),k ))
    
    def calculate_shortest_routes(self, alice, bob):
        """
        Procura a rota de menor custo.
        Args:
            alice, bob (node): Nós do grafo da rede.

        Returns:
            route (list): Lista de nós que compõem a rota.
        """
        return list(nx.all_shortest_paths(self.network.G, alice, bob))
    
    def allocate_routes(self, request_list, routes_calculation_type='shortest'):
        """
        Aloca as rotas para os pedidos e atualiza a lista de requisições.
        
        Args:
            request_list (list): Lista de requisições -> [alice, bob, app].
        
        Returns:
            info (list): Lista de dicionários -> [{'Priority': priority, 'Route': route, 'App': app}].
        """

        # Informações das requisições
        info = []
        # Todos os links já utilizados
        all_used_links = set()
        # Links utilizados apenas por BB84 e B92
        bb84_b92_used_links = set()
        # Contador de rotas E91 (para que não haja muitos E91 com links compartilhados)
        e91_count = 0
        # Ordenando as requisições por prioridade
        sorted_request_list = sorted(request_list, key=lambda x: x[3], reverse=True)
                        
        for alice, bob, app, priority in sorted_request_list:
            
            # Calcula as rotas de menor custo
            if routes_calculation_type == 'shortest':
                routes = self.calculate_shortest_routes(alice, bob)
            elif routes_calculation_type == 'kshortest': 
                routes = self.calculate_k_shortest_routes(alice, bob)
            elif routes_calculation_type == 'all':
                routes = self.calculate_all_routes(alice, bob)
                
            # Itera sobre as rotas
            for route in routes:
                # Lista de pares de elementos adjacentes da lista route (canais)
                route_links = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
                # Checa se nenhum link dessa rota já foi usado em uma rota anterior
                if not any(link in all_used_links for link in route_links):
                        # Se a app for BB84 ou B92, adiciona os links usados no conjunto de links usados apenas por essas apps
                        if app == 'BB84' or app == 'B92':
                            bb84_b92_used_links.update(route_links)
                        
                        # Adicionando as informações de rota, app e prioridade
                        info.append({'Priority': priority, 'Route': route, 'App': app})
                        
                        # Adiciona os links usados no conjunto de links usados
                        all_used_links.update(route_links)
                        
                        # Remove a requisição da lista de requisições
                        request_list.remove((alice, bob, app, priority))
                        
                        break
                    
                elif app == 'E91':
                    # Se nenhum dos links desta rota está nos links utilizados pelos outros tipos de protocolo, os links que estão sendo utilizados são dos outros E91
                    if not any(e91_link in bb84_b92_used_links for e91_link in route_links):
                        # Para que não haja tantos E91 com links compartilhados, só 3 rotas E91 que compartilham links serão alocadas no máximo
                        if e91_count < 3:
                            # Adicionando as informações de rota, app e prioridade
                            info.append({'Priority': priority, 'Route': route, 'App': app})
                            
                            # Adicionando o link ao conjunto de links usados
                            all_used_links.update(route_links)
                            
                            # Removendo a requisição da lista de requisições
                            request_list.remove((alice, bob, app, priority))
                            e91_count += 1
                        
                        break
        
        return info
    
    def send_requests(self, request_list, routes_calculation_type='shortest'):
        """
        Envia as requisições para a rede que as executa a partir da lista.
        
        Args:
            request_list (list): Lista de requisições -> [alice, bob, app].
        """

        # Índice da execução
        exec_index = 1
        results = dict()
        
        # Enquanto houver requisições na lista de requisições
        while len(request_list) > 0:
            # Alocando as rotas para os pedidos possíveis de serem atendidos, ou seja, que não compartilham links
            requests_info = self.allocate_routes(request_list, routes_calculation_type)
                        
            #LOG
            #print(f'{exec_index}ª execução.')
            #print(f'Rotas alocadas: {allocated_routes}')
            #print(f'Apps: {list_app}')
            
            
            for request in requests_info:
                # Informações da requisição
                alice, bob = request["Route"][0], request["Route"][-1]
                app = request["App"]
                route = request["Route"]
                
                # Executa a aplicação QKD
                if app == 'B92':
                    exec_data = run_qkd_b92(self.network, route)
                elif app == 'BB84':
                    exec_data = run_qkd_bb84(self.network, route)
                elif app == 'E91':
                    exec_data = run_qkd_e91(self.network, route)
            
            # Coletando dados
            results[exec_index] = exec_data
            exec_index += 1
        
        return results