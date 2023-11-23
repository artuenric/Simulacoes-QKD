# Dependências gerais
import random
from components.qubit import Qubit

# Funções gerais
from components.qkd.app import *

# Protocolo BB84
def prepara_qubits_bb84(key, bases):
    """
    Prepara os qubits de acordo com a chave clássica gerada.

    Args:
        key (lista): Lista de 0s e 1s com a chave.
        bases (lista): Lista de 0s e 1s com as bases.
    
    Returns:
        results (list): Lista com resultados das medições dos qubits.
    """
    
    qubits = []
    
    for bit, base in zip(key, bases):
        qubit = Qubit()
        if bit == 1:
            qubit.X()
        if base == 1:
            qubit.H()
        qubits.append(qubit)
        
    return qubits

def aplly_bases_in_measurement_bb84(qubits, bases):
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