from components.qkd.b92 import *
from components.qkd.bb84 import *
from components.qkd.e91 import *

# QKD B92
def run_qkd_b92(network, route):
    """
    Executa o protocolo QKD B92.

    Args:
        rede (Network): Rede em que o protocolo será executado.
        controller (Controller): Controlador da rede.
        alice (networkx node): Nó remetente das chaves.
        bob (networkx node): Nó destinatário das chaves.
        num_keys (int, optional): Número de chaves geradas. Defaults to 100.

    Returns:
        Dict : Dicionário de dicionários com as informações das execuções.
    """
    # Número de qubits para geração da chave
    nqubits = network.nqubits
    
    # Informações para Alice
    key_alice = create_key(nqubits)
    
    # Qubits
    qubits = prepara_qubits_b92(key_alice)
    
    # Informações para Bob
    bases_bob = generate_bases(nqubits)
    
    # Enviando os qubits
    bob_received_qubits, interference_qubits = network.send_qubits(route, qubits)
    
    # Bob mede os qubits
    key_bob = apply_measurement_b92(bob_received_qubits, bases_bob)
    
    # Qubits sem interferência
    shared_key = check_key(key_bob, key_alice)
    
    
    # Resultados da execução
    results = dict()
    results['app'] = 'B92'
    results['generated key'] = key_alice
    results['shared key'] = shared_key
    results['different bits'] = len(key_alice) - len(shared_key)
    results['key sucess'] = len(shared_key) / nqubits

    return results

# QKD BB84
def run_qkd_bb84(network, route):
    """
    Executa o protocolo QKD BB84.

    Args:
        network (Network): Rede em que o protocolo será executado.
        controller (Controller): Controlador da rede.
        alice (networkx node): Nó remetente das chaves.
        bob (networkx node): Nó destinatário das chaves.
        num_keys (int, optional): Número de chaves geradas. Defaults to 100.

    Returns:
        Dict : Dicionário de dicionários com as informações das execuções.
    """
    # Número de qubits para geração da chave
    nqubits = network.nqubits
    
    # Informações para Alice
    key_alice = create_key(nqubits)
    
    bases_alice = generate_bases(nqubits)
    
    # Qubits
    qubits = prepara_qubits_bb84(key_alice, bases_alice)
    
    # Informações para Bob
    bases_bob = generate_bases(nqubits)
    
    # Enviando os qubits
    received_qubits, interference_qubits = network.send_qubits(route, qubits)
    
    # Bob mede os qubits
    measured_qubits = aplly_bases_in_measurement_bb84(received_qubits, bases_bob)
    
    # Comparando as bases de Alice e Bob
    matching_bases = compare_bases(bases_alice, bases_bob)
    
    # Chave obtida de acordo com as bases
    key_bob = get_key(measured_qubits, matching_bases)
    
    # Checando a chave
    shared_key = check_key(key_bob, key_alice)

    # Resultados da execução
    results = dict()
    results['app'] = 'BB84'
    results['generated key'] = key_alice
    results['shared key'] = shared_key
    results['different bits'] = len(key_alice) - len(shared_key)
    results['key sucess'] = len(shared_key) / nqubits
    
    # Resultados
    return results

# QKD E91
def run_qkd_e91(network, route):
    """
    Executa o protocolo QKD E91.

    Args:
        network (Network): Rede em que o protocolo será executado.
        controller (Controller): Controlador da rede.
        alice (networkx node): Nó remetente das chaves.
        bob (networkx node): Nó destinatário das chaves.

    Returns:
        Dict : Dicionário de dicionários com as informações das execuções.
    """
    # Número de qubits para geração da chave
    nqubits = network.nqubits    
    
    # Informações para Alice
    key_alice = create_key(nqubits)
    bases_alice = generate_bases(nqubits)
    
    # Eprs
    pairs = prepara_qubits_e91(key_alice, bases_alice)
    
    # Informações para Bob
    bases_bob = generate_bases(nqubits)
    
    # Enviando os qubits
    received_qubits, interference_qubits = network.send_eprs(route, pairs)
    
    # Bob medindo os qubits
    measured_qubits = aplly_bases_in_measurement_e91(received_qubits, bases_bob)
    
    # Comparando as bases de Alice e Bob
    matching_bases = compare_bases(bases_alice, bases_bob)
    
    # Chave obtida de acordo com as bases
    key_bob = get_key(measured_qubits, matching_bases)
    
    # Chave obtida de acordo com as bases
    key_bob = get_key(measured_qubits, matching_bases)
    
    # Checando chave
    shared_key = check_key(key_bob, key_alice)
    
    # Resultados da execução
    results = dict()
    results['app'] = 'E91'
    results['generated key'] = key_alice
    results['shared key'] = shared_key
    results['different bits'] = len(key_alice) - len(shared_key)
    results['key sucess'] = len(shared_key) / nqubits
    
    return results    