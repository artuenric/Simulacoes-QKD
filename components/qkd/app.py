import random
from components.qkd.request import Request

# Funções básicas compartilhadas entre os protocolos
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
        else:
            bob_key.append(None)
            
    return bob_key
   
def check_key(key_bob, key_alice):
    """
    Compara as chaves de Alice e Bob.

    Args:
        key_alice (list): Chave gerada por Alice.
        key_bob (list): Chave obtida por Bob.
    """
    shared_key = []

    for bob_bit, alice_bit in zip(key_bob, key_alice):
        if bob_bit != None:
            if bob_bit == alice_bit:
                shared_key.append(bob_bit)
    
    return shared_key

# Funções para simulação
def generate_qkd_requests(rede, num_requests, apps, case):
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
            raise ValueError("Invalid case parameter")
            
        for i in range(num_requests):
            classe = random.choices(classes, class_distribution)[0]
            app = random.choice(apps)
            priority = random.randint(1, 5)
            alice, bob = rede.random_alice_bob()
            r = Request(classe, app, priority, alice, bob)
            requests.append(r)
        return requests

def run_simulations(rede, controlador, n_simulacoes, n_requests, apps, caso, routes_calculation_type):
    """
    Roda as simulações para os protocolos BB84, E91 e B92.

    Args:
        rede (Network): Rede.
        controlador (Controller): Controlador.
        n_simulacoes (int): Número de simulações.
        n_requests (int): Número de requisições.
        routes_calculation_type (str): Tipo de roteamento.
    
    Returns:
        taxas_sucesso_chaves_geral (list): Lista com as taxas de sucesso das chaves para cada simulação.
        vazao (list): Lista com a vazão para cada simulação.
    """
    
    # Variáveis para armazenar os resultados
    taxas_sucesso_chaves_geral = []
    vazao = []

    # Rodando as simulações
    for simulacao in range(n_simulacoes):
        taxas_sucesso_chaves_e91 = []
        taxas_sucesso_chaves_bb84 = []
        taxas_sucesso_chaves_b92 = []
        
        requests = generate_qkd_requests(rede, n_requests, apps, caso)
        resultados_simulacao = controlador.send_requests(requests, routes_calculation_type)
        
        for indice_execucao in resultados_simulacao:
            resultado_individual_simulacao = resultados_simulacao[indice_execucao]
            sucesso_chave = resultado_individual_simulacao['key sucess']

            if resultado_individual_simulacao['app'] == 'BB84':
                taxas_sucesso_chaves_bb84.append(sucesso_chave)
                
            elif resultado_individual_simulacao['app'] == 'E91':
                taxas_sucesso_chaves_e91.append(sucesso_chave)
                
            elif resultado_individual_simulacao['app'] == 'B92':
                taxas_sucesso_chaves_b92.append(sucesso_chave)

        # Salvando o sucesso nas chaves geral da simulação
        lista_combinada = [taxa for sublist in [taxas_sucesso_chaves_bb84, taxas_sucesso_chaves_e91, taxas_sucesso_chaves_b92] for taxa in sublist]
        taxas_sucesso_chaves_geral.append(sum(lista_combinada) / len(lista_combinada))
        
        # Calculando a vazão
        n_execucoes = len(resultados_simulacao)
        vazao.append(n_requests / n_execucoes)

    return vazao, taxas_sucesso_chaves_geral

# Funções para plotagem
def formatar_numero(numero):
    """
    Ajuda a formatar um número para coloca-lo em uma tabela.

    Args:
        numero (int): Número a ser formatado.

    Returns:
        str: Número formatado.
    """
    # Transforma o número em uma string com 7 casas decimais
    numero_formatado = "{:.7f}".format(numero)

    # Substitui o ponto pela vírgula
    numero_formatado = numero_formatado.replace('.', ',')

    return numero_formatado