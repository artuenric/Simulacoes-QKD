import random
from ..request import Request
class Simulation:
    def __init__(self, network, controller) -> None:
        self.network = network
        self.controller = controller
        self.case = None
        self.requests = []
        self.apps = ["BB84", "E91", "B92"]
        self.apps_distribution = [0.33, 0.33, 0.33]
        
    def generate_requests(self, num_requests, case):
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
        
        if case == 1:
            class_distribution = [0.3, 0.3, 0.2, 0.15, 0.05]
        elif case == 2:
            class_distribution = [0.25, 0.25, 0.2, 0.15, 0.15]
        elif case == 3:
            class_distribution = [0.2] * 5
        elif case == 4:
            class_distribution = [0.15, 0.15, 0.2, 0.25, 0.25]       
        elif case == 5:
            class_distribution = [1, 0, 0, 0, 0]
        elif case == 6:
            class_distribution = [0, 1, 0, 0, 0]
        elif case == 7:
            class_distribution = [0, 0, 1, 0, 0]
        elif case == 8:
            class_distribution = [0, 0, 0, 1, 0]
        elif case == 9:
            class_distribution = [0, 0, 0, 0, 1]
        else:
            raise ValueError("Invalid case parameter")
        
        # Gera as requisições
        for i in range(num_requests):
            classe = random.choices(classes, class_distribution)[0]
            app = random.choices(self.apps, self.apps_distribution)[0]
            priority = random.randint(1, 5)
            alice, bob = self.network.random_alice_bob()
            r = Request(classe, app, priority, alice, bob)
            requests.append(r)
            
        return requests

    def run(self, num_requests, case):
        pass