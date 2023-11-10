import networkx as nx
from components.protocols import *

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
    
    def allocate_routes(self, request_list):
        """
        Aloca as rotas para os pedidos. E atualiza a lista de requisições.
        
        Args:
            request_list (list): Lista de requisições -> [alice, bob, app].
        """
        allocated_routes = []
        all_used_links = set()
        bb84_b92_used_links = set()
        e91_count = 0
        list_app = []
                
        for alice, bob, app in request_list.copy():
            # Calcula a rota de menor custo
            route = self.calculate_route(alice, bob)
            
            # Lista de pares de elementos adjacentes da lista route
            route_links = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
            
            # Checa se nenhum link dessa rota já foi usado em uma rota anterior
            if not any(link in all_used_links for link in route_links):
                    # Se a app for BB84 ou B92, adiciona os links usados no conjunto de links usados apenas por essas apps
                    if app == 'BB84' or app == 'B92':
                        bb84_b92_used_links.update(route_links)
                    
                    # Adiciona a rota e o app na lista de rotas alocadas
                    allocated_routes.append(route)
                    list_app.append(app)
                    
                    # Adiciona os links usados no conjunto de links usados
                    all_used_links.update(route_links)
                    
                    # Remove a requisição da lista de requisições
                    request_list.remove((alice, bob, app))
            
            elif app == 'E91':
                # Se nenhum dos links desta rota está nos links utilizados pelos outros tipos de protocolo, os links que estão sendo utilizados são dos outros E91
                if not any(e91_link in bb84_b92_used_links for e91_link in route_links):
                    # Para que não haja tantos E91 com links compartilhados, só 3 rotas E91 que compartilham links serão alocadas no máximo
                    if e91_count < 3:
                        allocated_routes.append(route)
                        list_app.append(app)
                        all_used_links.update(route_links)
                        request_list.remove((alice, bob, app))
                        e91_count += 1
                        
        return allocated_routes, list_app
    
    def send_requests(self, request_list):
        """
        Envia as requisições para a rede que as executa a partir da lista.
        
        Args:
            request_list (list): Lista de requisições -> [alice, bob, app].
        """

        # 
        exec_index = 1
        results = dict()
        
        # Enquanto houver requisições na lista de requisições
        while len(request_list) > 0:
            # Alocando as rotas para os pedidos possíveis de serem atendidos, ou seja, que não compartilham links
            allocated_routes, list_app = self.allocate_routes(request_list)
                        
            # Printando as informações da execução
            #print(f'{exec_index}ª execução.')
            #print(f'Rotas alocadas: {allocated_routes}')
            #print(f'Apps: {list_app}')
            
            for route, app in zip(allocated_routes, list_app):
                # Alice é o primeiro elemento da rota e Bob é o último
                alice, bob = route[0], route[-1]
                qkd_app = app
                
                # Executa a aplicação QKD
                if qkd_app == 'B92':
                    exec_data = run_qkd_b92(self.network, self, alice, bob)
                elif qkd_app == 'BB84':
                    exec_data = run_qkd_bb84(self.network, self, alice, bob)
                elif qkd_app == 'E91':
                    exec_data = run_qkd_e91(self.network, self, alice, bob)

            # Coletando dados
            results[exec_index] = exec_data
            
            exec_index += 1
        
        return results