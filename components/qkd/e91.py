import random
from components.qubit import Qubit
from components.epr import Epr

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

def prepara_qubits_e91(key, bases):
    """
    Prepara os qubits de acordo com a chave clássica gerada.

    Args:
        key (lista): Lista de 0s e 1s com a chave.
        bases (lista): Lista de 0s e 1s com as bases.
        
    Returns:
        results (list): Lista com resultados das medições dos qubits.
    """
    
    pairs = []
    
    for bit, base in zip(key, bases):
        epr = Epr()
        if bit == 1:
            epr.X()
        if base == 1:
            epr.H()
        pairs.append(epr)
        
    return pairs

def aplly_bases_in_measurement_e91(qubits, bases):
    """
    Mede os qubits a partir das bases já definidas.

    Args:
        qubits (list): Lista de Qubits.
        bases (list): Lista com 0s e 1s.
    """
    
    measurement = 0
    results = []
    for qubit, base, in zip(qubits, bases):
        if base == 1:
            qubit.H()
        measurement = qubit.measure()
        results.append(measurement)
    
    return results

def get_key(measured_qubits, match_bases):
    """
    Filtra a lista com os resultados das medições para somente aquelas que as bases deram match.
    
    Args:
        match_bases (lista): Lista com as bases que deram match.
        measured_qubits (lista): Lista com os resultados das medições dos qubits.
    
    Returns:
        shared_key (list): Chave compartilhada utilizável.
    """
    
    shared_key = []
    
    for qubit, base in zip(measured_qubits, match_bases):
        if base:
            shared_key.append(qubit)
    
    return shared_key