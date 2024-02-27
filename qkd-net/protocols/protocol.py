# Classe mãe
# BB84, E91, B92 serão filhas
# Onde eu vou pôr esse Protocol??????????
# Agora o protocolo acessa o tamanho das cahves pela rede. Talvez trocar isso...

import random 
from abc import ABC, abstractmethod
class Protocol(ABC):
    """
    Protocolo QKD.
    """
    def __init__(self) -> None:
        self.app = None
        self.alice = None
        self.bob = None
        self.generated_key = None
        self.shared_key = None
        self.different_bits = None
        self.key_sucess = None
    
    def create_key(self, size):
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
    
    def generate_bases(self, size):
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

    @abstractmethod
    def prepare_qubits(self):
        pass
    
    @abstractmethod
    def apply_measurement(self):
        pass
    
    @abstractmethod
    def check_key(self):
        pass
    
    @abstractmethod
    def run(self):
        pass
    
    # Implementar as ações realizadas pelos protocolos