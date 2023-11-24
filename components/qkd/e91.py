# Dependências gerais
import random
from components.qubit import Qubit
from components.epr import Epr

# Funções gerais
from components.qkd.app import *

# Protocolo E91
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

    for qubit, base in zip(qubits, bases):
        if base == 1:
            qubit.H()
        measurement = qubit.measure()
        results.append(measurement)
    
    return results