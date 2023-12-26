import networkx as nx
from components.protocols import *
from itertools import islice

class Controller():
    """
    Um objeto que atua como Controlador SDN para a rede quântica.
    """
    def __init__(self, network) -> None:
        self.network = network
    
    def set_network(self, network):
        """
        Define a rede que o controlador trabalha.  
        
        Args:
            network (Network): Rede em que o controlador atua.
        """
        self.network = network
        network.set_controller(self)
    
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
    
    
    def dfs_paths(self, source, target, length, path=None):
        """
        Realiza uma busca em profundidade (DFS) em busca de caminhos de um comprimento específico entre dois nós.

        Args:
            source (node): Nó de origem.
            target (node): Nó de destino.
            length (int): Comprimento desejado do caminho.
            path (list, optional): Caminho parcial atual. Defaults to None.

        Yields:
            list: Lista de nós que compõem um caminho de comprimento específico entre source e target.
        """
        G = self.network.G
         # Inicializa o caminho se não estiver definido
        if path is None:
            path = [source]
        # Verifica se o comprimento do caminho atingiu o objetivo
        if len(path) == length:
            if path[-1] == target:
                yield path
            return
        # Explora os vizinhos do nó de origem
        for neighbor in G.neighbors(source):
            # Garante que o vizinho não esteja no caminho atual
            if neighbor not in path:
                # Recursivamente busca caminhos a partir do vizinho
                yield from self.dfs_paths(neighbor, target, length, path + [neighbor])

    def calculate_routes_of_k_length(self, source, target, length):
        """
        Encontra todos os caminhos de um comprimento específico entre dois nós.

        Args:
            source (node): Nó de origem.
            target (node): Nó de destino.
            length (int): Comprimento desejado do caminho.

        Returns:
            list: Lista de caminhos entre source e target com o comprimento especificado.
        """
         # Chama a função de busca em profundidade com comprimento + 1 porque length inclui o nó de origem
        return list(self.dfs_paths(source, target, length + 1))

    def calculate_shortest_routes(self, alice, bob):
        """
        Procura a rota de menor custo.
        Args:
            alice, bob (node): Nós do grafo da rede.

        Returns:
            route (list): Lista de nós que compõem a rota.
        """
        return list(nx.all_shortest_paths(self.network.G, alice, bob))
    
    def send_requests(self, request_list, routes_calculation_type):
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
            #LOG
            print(f'{exec_index}ª EXECUÇÃO:')
            print("Requisições: ", list(r.__str__() for r in request_list))
            # Alocando as rotas para os pedidos possíveis de serem atendidos, ou seja, que não compartilham links
            requests_info = self.allocate_routes(request_list, routes_calculation_type)
            
            for request in requests_info:
                # Executa a aplicação QKD
                if request.app == 'B92':
                    exec_data = run_qkd_b92(self.network, request.route)
                elif request.app == 'BB84':
                    exec_data = run_qkd_bb84(self.network, request.route)
                elif request.app == 'E91':
                    exec_data = run_qkd_e91(self.network, request.route)
                # Atualizando a chave obtida pelo request
                request.update_keys(len(exec_data['shared key']))
                # Atualiza a lista de requisições
                if request.keys <= 0:
                    request_list.remove(request)
            
            # Coletando dados
            results[exec_index] = exec_data
            
            exec_index += 1
        
        return results
    
    def allocate_routes(self, request_list, routes_calculation_type):
        """
        Aloca as rotas para os pedidos e atualiza a lista de requisições.
        
        Args:
            request_list (list): Lista de requisições -> [alice, bob, app].
            routes_calculation_type (str): shortest, kshortest, all, klength.
            
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
        sorted_request_list = sorted(request_list, key=lambda x: x.priority , reverse=True)
        print("Requests ordenados por prioridade: ", list(r.__str__() for r in sorted_request_list))
        for request in sorted_request_list:
            # Calcula as rotas de menor custo
            if routes_calculation_type == 'shortest':
                routes = self.calculate_shortest_route(request.alice, request.bob)
            elif routes_calculation_type == 'kshortest': 
                routes = self.calculate_k_shortest_routes(request.alice, request.bob)
            elif routes_calculation_type == 'all':
                routes = self.calculate_all_routes(request.alice, request.bob)
            elif routes_calculation_type == 'klength':
                routes = self.calculate_routes_of_k_length(request.alice, request.bob, 5)
            
            print(f'Rotas: {routes}')
            # Itera sobre as rotas
            for route in routes:
                #print(f'Rota Avaliada: {route}')
                # Lista de pares de elementos adjacentes da lista route (canais)
                route_links = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
                print("Rota atual trabalhada: ", route)
                # Checa se nenhum link dessa rota já foi usado em uma rota anterior
                if not any(link in all_used_links for link in route_links):
                        # Se a app for BB84 ou B92, adiciona os links usados no conjunto de links usados apenas por essas apps
                        if request.app == 'BB84' or request.app == 'B92':
                            bb84_b92_used_links.update(route_links)
                        
                        # Adicionando as informações de rota, app e prioridade
                        request.route = route
                        info.append(request)
                        
                        # Adiciona os links usados no conjunto de links usados
                        all_used_links.update(route_links)
 
                        break
                    
                elif request.app == 'E91':
                    # Se nenhum dos links desta rota está nos links utilizados pelos outros tipos de protocolo, os links que estão sendo utilizados são dos outros E91
                    if not any(e91_link in bb84_b92_used_links for e91_link in route_links):
                        # Para que não haja tantos E91 com links compartilhados, só 3 rotas E91 que compartilham links serão alocadas no máximo
                        if e91_count < 3:
                            # Adicionando as informações de rota, app e prioridade
                            request.route = route
                            info.append(request)
                            
                            # Adicionando o link ao conjunto de links usados
                            all_used_links.update(route_links)

                            e91_count += 1
                        
                        break
        
        return info