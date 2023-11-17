
import random

def generate_qkd_request(rede, num_requests, diff_nodes=5):
        """
        Gera uma lista de requisições aleatórias de QKD.

        Args:
            num_requests (int): Número de requisições.
            diff_nodes (int): Número entre os nós. Defauts to 5.

        Returns:
            requests (list): Lista com requisições.
        """
        requests = []
        avaliable_apps = ["B92"]
        
        for i in range(num_requests):
            alice, bob = rede.random_alice_bob(diff_nodes)
            
            app = random.choice(avaliable_apps)
            requests.append((alice, bob, app))
        
        return requests
    