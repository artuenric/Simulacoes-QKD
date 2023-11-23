# Dependências gerais
import random
from components.qubit import Qubit

# Funções gerais
from components.qkd.app import *

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

def apply_measurement_b92(qubits, bases):
    """
    Mede os qubits a partir das bases já definidas.

    Args:
        qubits (list): Lista de Qubits.
    
    Returns:
        results (list): Lista com resultados das medições dos qubits.
    """
    
    results = []
    result = 0
    measure = 0
    
    for qubit, base in zip(qubits, bases):
        # Aplica a base
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
        # Caso o resultado seja  0, não é possível saber se o qubit foi enviado como 0 ou 1
        else:
            results.append(None)
        
    return results

def check_key(key_bob, indexs):
    """
    Compara as chaves de Alice e Bob.

    Args:
        key_bob (list): Chave obtida por Bob.
        indexs (list): Lista com os índices dos qubits que sofreram interferência.
    """
    shared_key = []
    
    for bit in key_bob:
        if bit != None:
            if key_bob.index(bit) not in indexs:
                shared_key.append(bit)
    
    return shared_key