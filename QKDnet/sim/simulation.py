import random
from ..request import Request

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
        self.max_time_request = None
        # Resultados
        self.throughputs = []
        self.throughput = 0
        self.key_sucess_rate = []
        self.key_sucess_rate = 0
        
    
    # Implementados futuramente:
    
    # def set_apps(self, apps):
        # """
        # Define as apps disponíveis para a simulação.

        # Args:
        #     apps (list): Lista com os nomes das apps disponíveis.
        # """
        # self.apps = apps
        
    # def set_n_simulations(self, n):
    #     """
    #     Define o número de simulações.

    #     Args:
    #         n (int): Número de simulações.
    #     """
    #     pass
    
    def set_case(self, case):
        """
        Define o caso para simulação. Os casos vão de 1 a 9. Representam as diferentes formas de distribuição das classes.

        Args:
            case (int): Caso escolhido para a simulação.
        """
        self.case = case
    
    def set_n_requests(self, n):
        """
        Define o número de requests.

        Args:
            n (int): Número de requests.
        """
        self.n_requests = n
    
    def set_apps_distribution(self, distribution):
        """
        Define a distribuição de probabilidade para as apps disponíveis.

        Args:
            distribution (list): Lista com a distribuição. Respectivamente para BB84, E91, B92.
        """
        self.apps_distribution = distribution
    
    def set_max_time_request(self, time):
        """
        Define o tempo máximo (em time slot) para o request ser atendido.
        
        Args:
            time (int): Tempo máximo para o request ser atendido.
        """
    
        self.max_time_request = time
    
    def get_key_success_rate(self):
        """
        Retorna a taxa de sucesso da chave.

        Returns:
            float: Taxa de sucesso da chave.
        """
        return self.key_sucess_rate
    
    def get_throughput(self):
        """
        Retorna a vazão.

        Returns:
            float: Vazão.
        """
        return self.throughput
    
    def clear_data(self):
        """
        Limpa os dados coletados das simulações.
        """
        self.controller.data_base.clear_data()
        self.key_sucess_rate = 0
        self.throughput = 0
        
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
            r = Request(i, classe, app, priority, random.randint(5, 15), alice, bob)
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
        self.key_sucess_rate = self.controller.data_base.get_key_sucess_rate()
    
    def multi_run(self):
        """
        Roda várias simulações.

        Args:
            n_simulations (int): Número de simulações.
            n_requests (int): Número de requisições.
            routes_calculation_type (str): Tipo de roteamento.
        
        Returns:
            taxas_sucesso_chaves_geral (list): Lista com as taxas de sucesso das chaves para cada simulação.
            vazao (list): Lista com a vazão para cada simulação.
        """
        for i in range(self.n_simulations):
            self.run()
            self.throughputs.append(self.throughput)
            self.key_sucess_rate.append(self.key_sucess_rate)
            self.controller.data_base.clear_data()
        
        return self.key_sucess_rate, self.throughputs