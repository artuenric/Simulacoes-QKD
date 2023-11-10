from components.qkd.b92 import *
from components.qkd.bb84 import *
from components.qkd.e91 import *

# QKD B92
def run_qkd_b92(network, controller, alice, bob, key_size=100):
    """
    Executa o protocolo QKD B92.

    Args:
        rede (Network): Rede em que o protocolo será executado.
        controller (Controller): Controlador da rede.
        alice (networkx node): Nó remetente das chaves.
        bob (networkx node): Nó destinatário das chaves.
        num_keys (int, optional): Número de chaves geradas. Defaults to 100.
        key_size (int, optional): Tamanho das chaves geradas. Defaults to 100.

    Returns:
        Dict : Dicionário de dicionários com as informações das execuções.
    """
    # Informações para Alice
    key_alice = create_key(key_size)
    
    # Qubits
    qubits = prepara_qubits_b92(key_alice)
    
    # Calculando a rota
    route = controller.calculate_route(alice, bob)

    # Bob recebendo a chave
    received_qubits = network.send_qubits(route, qubits)
    
    # Bob mede os qubits
    measured_qubits, bases_bob = apply_measurement_b92(received_qubits)
    diff_bits = len(key_alice) - len(measured_qubits)
    
    # Resultados da execução
    results = dict()
    results['generated key'] = key_alice
    results['shared key'] = measured_qubits
    results['different bits'] = diff_bits
    results['key sucess'] = len(measured_qubits) / key_size

    return results

# QKD BB84
def run_qkd_bb84(network, controller, alice, bob, key_size=100):
    """
    Executa o protocolo QKD BB84.

    Args:
        network (Network): Rede em que o protocolo será executado.
        controller (Controller): Controlador da rede.
        alice (networkx node): Nó remetente das chaves.
        bob (networkx node): Nó destinatário das chaves.
        num_keys (int, optional): Número de chaves geradas. Defaults to 100.
        key_size (int, optional): Tamanho das chaves geradas. Defaults to 100.

    Returns:
        Dict : Dicionário de dicionários com as informações das execuções.
    """
    # Informações para Alice
    key_alice = create_key(key_size)
    bases_alice = generate_bases(key_size)
    
    # Qubits
    qubits = prepara_qubits_bb84(key_alice, bases_alice)
    
    # Informações para Bob
    bases_bob = generate_bases(key_size)
    
    # Calculando a rota
    route = controller.calculate_route(alice, bob)

    # Bob recebendo a chave
    received_qubits = network.send_qubits(route, qubits)
    
    # Bob mede os qubits
    measured_qubits = aplly_bases_in_measurement_bb84(received_qubits, bases_bob)
    
    # Comparando as bases de Alice e Bob
    matching_bases = compare_bases(bases_alice, bases_bob)
    
    # Chave obtida de acordo com as bases
    generated_shared_key = get_key(measured_qubits, matching_bases)

    # Resultados da execução
    results = dict()
    results['generated key'] = key_alice
    results['shared key'] = generated_shared_key
    results['different bits'] = len(key_alice) - len(measured_qubits)
    results['key sucess'] = len(generated_shared_key) / key_size
    
    # Resultados
    return results

# QKD E91
def run_qkd_e91(network, controller, alice, bob, key_size=100):
    """
    Executa o protocolo QKD E91.

    Args:
        network (Network): Rede em que o protocolo será executado.
        controller (Controller): Controlador da rede.
        alice (networkx node): Nó remetente das chaves.
        bob (networkx node): Nó destinatário das chaves.
        key_size (int, optional): Tamanho das chaves geradas. Defaults to 100.

    Returns:
        Dict : Dicionário de dicionários com as informações das execuções.
    """
    # Informações para Alice
    key_alice = create_key(key_size)
    bases_alice = generate_bases(key_size)
    
    # Qubits
    qubits = prepara_qubits_e91(key_alice, bases_alice)
    
    # Informações para Bob
    bases_bob = generate_bases(key_size)
    
    # Calculando a rota
    route = controller.calculate_route(alice, bob)
    
    # Bob recebendo a chave
    received_qubits = network.send_eprs(route, qubits)
    
    # Bob mede os qubits
    measured_qubits = aplly_bases_in_measurement_e91(received_qubits, bases_bob)
    
    # Comparando as bases de Alice e Bob
    matching_bases = compare_bases(bases_alice, bases_bob)
    
    # Chave obtida de acordo com as bases
    generated_shared_key = get_key(measured_qubits, matching_bases)
    
    # Resultados da execução
    results = dict()
    results['generated key'] = key_alice
    results['shared key'] = generated_shared_key
    results['different bits'] = len(key_alice) - len(measured_qubits)
    results['key sucess'] = len(generated_shared_key) / key_size
    
    return results    