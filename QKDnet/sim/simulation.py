import random
from ..request import Request

###

rs = []
rs.append(Request(0, "Class A", "BB84", 5, 0, 10))
rs.append(Request(1, "Class B", "BB84", 5, 2, 4))
rs.append(Request(3, "Class D", "BB84", 5, 2, 5))
rs.append(Request(4, "Class E", "BB84", 5, 5, 6))
rs.append(Request(2, "Class C", "BB84", 5, 1, 3))

####

class Simulation:
    def __init__(self, network, controller) -> None:
        # Propriedades
        self.network = network
        self.controller = controller
        self.requests = []
        # Condigurações
        self.n_simulations = None
        self.n_requests = None
        self.case = None
        self.apps = ["BB84", "E91", "B92"]
        self.apps_distribution = [0.33, 0.33, 0.33]
        # Resultados
        self.throughput = None
        self.sucess_rate = None
        
    def generate_requests(self):
        """
        Gera uma lista de requisições aleatórias de QKD.

        Args:
            num_requests (int): Número de requisições.
            diff_nodes (int): Número entre os nós. Defauts to 5.
            apps (list): Lista de apps disponíveis.
            
        Returns:
            requests (list): Lista com requisições.
        """
        classes = ["Class A", "Class B", "Class C", "Class D", "Class E"]
        requests = []
        
        if self.case == 1:
            class_distribution = [0.3, 0.3, 0.2, 0.15, 0.05]
        elif self.case == 2:
            class_distribution = [0.25, 0.25, 0.2, 0.15, 0.15]
        elif self.case == 3:
            class_distribution = [0.2] * 5
        elif self.case == 4:
            class_distribution = [0.15, 0.15, 0.2, 0.25, 0.25]       
        elif self.case == 5:
            class_distribution = [1, 0, 0, 0, 0]
        elif self.case == 6:
            class_distribution = [0, 1, 0, 0, 0]
        elif self.case == 7:
            class_distribution = [0, 0, 1, 0, 0]
        elif self.case == 8:
            class_distribution = [0, 0, 0, 1, 0]
        elif self.case == 9:
            class_distribution = [0, 0, 0, 0, 1]
        else:
            raise ValueError("Invalid case parameter")
        
        # Gera as requisições
        for i in range(self.n_requests):
            classe = random.choices(classes, class_distribution)[0]
            app = random.choices(self.apps, self.apps_distribution)[0]
            priority = random.randint(1, 5)
            alice, bob = self.network.random_alice_bob()
            r = Request(i, classe, app, priority, alice, bob)
            requests.append(r)
            
        return requests

    def run(self):
        """
        Roda as simulações para os protocolos BB84, E91 e B92.

        Args:
            rede (Network): Rede.
            controlador (Controller): Controlador.
            n_simulacoes (int): Número de simulações.
            n_requests (int): Número de requisições.
            routes_calculation_type (str): Tipo de roteamento.
        
        Returns:
            taxas_sucesso_chaves_geral (list): Lista com as taxas de sucesso das chaves para cada simulação.
            vazao (list): Lista com a vazão para cada simulação.
        """
        # Rodando as simulações
        requests = self.generate_requests()
        # Adiciona as requisições ao controlador
        self.controller.receive_requests(requests)
        # Envia as requisições para a rede
        self.controller.send_requests()

        # Coleta os dados
        self.throughput = self.controller.data_base.get_throughput()
        self.sucess_rate = self.controller.data_base.get_key_sucess_rate()