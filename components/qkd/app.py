
import random

def create_key(size):
    """
    Gera uma lista de 0s e 1s para uma chave de criptografia.

    Args:
        size (int): Tamanho desejado para a chave.

    Returns:
        key (list): Uma lista com 0s e 1s aleatórios.
    """
    
    key = []
    
    for bit in range(size):
        key.append(random.randint(0, 1))
    
    return key

def generate_bases(size):
    """
    Gera uma lista com as bases escolhidas para realizar a medição dos qubits.
    
    Args:
        size (int): Tamanho da chave.
    """
    
    bases = []
    
    for base in range(size):
        bases.append(random.randint(0, 1))
    
    return bases

def compare_bases(base_alice, base_bob):
    """
    Compara as bases de Alice e Bob.
    Args:
        base_alice (list): Lista de 0s e 1s para as bases escolhidas por Alice.
        base_bob (list): Lista de 0s e 1s para as bases escolhidas por Bob.

    Returns:
        matching_bases (lista): Lista de Trues e Falses para representar o macth das bases.
    """
    
    matching_bases = []
    
    for a, b in zip(base_alice, base_bob):
        if a == b:
            matching_bases.append(True)
        else:
            matching_bases.append(False)
    
    return matching_bases

def get_key(measured_qubits, match_bases):
    """
    Filtra a lista com os resultados das medições para somente aquelas que as bases deram match.
    
    Args:
        match_bases (lista): Lista com as bases que deram match.
        measured_qubits (lista): Lista com os resultados das medições dos qubits.
    
    Returns:
        bob_key (list): Chave obtida por Bob.
    """
    
    bob_key = []
    
    for qubit, base in zip(measured_qubits, match_bases):
        if base:
            bob_key.append(qubit)
        
    return bob_key
   
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
    