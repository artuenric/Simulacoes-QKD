import random
from components.qubit import Qubit

# Funções gerais

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


# Protocolo B92

def prepara_qubits_b92(key):
    """
    Prepara os qubits de acordo com a chave clássica gerada.

    Args:
        key (lista): Lista de 0s e 1s com a chave.
    
    Returns:
        results (list): Lista com resultados das medições dos qubits.
    """
    
    qubits = []
    
    for bit in key:
        qubit = Qubit()
        if bit == 1:
            qubit.H()
        qubits.append(qubit)
        
    return qubits


def apply_measurement_b92(qubits):
    """
    Mede os qubits a partir das bases já definidas.

    Args:
        qubits (list): Lista de Qubits.
    
    Returns:
        results (list): Lista com resultados das medições dos qubits.
    """
    
    bases = []
    results = []
    result = 0
    measure = 0
    
    for qubit in qubits:
        
        base = random.randint(0, 1)
        bases.append(base)
        if base == 1:
            qubit.H()

        # Lógica do B92
        measure = qubit.measure()
        if measure == 1:
            if base == 1:
                result = 0
            elif base == 0:
                result = 1         
            results.append(result)
            
    return results, bases