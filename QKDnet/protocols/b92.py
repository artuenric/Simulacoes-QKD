from .protocol import Protocol
from ..quantum import Qubit

class B92(Protocol):
    def __init__(self, network):
        super().__init__()
        self.network = network
        self.app = "B92"
    
    def prepare_qubits(self, key):
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
    
    def apply_measurement(self, qubits, bases):
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
        
    def run(self, route):
        """
        Executa o protocolo QKD B92.

        Args:
            route (list): Lista com os nós da rota, de Alice até Bob.
            
        """
        # Número de qubits para geração da chave
        nqubits = self.network.nqubits
        
        # Informações para Alice
        key_alice = super().create_key(nqubits)
        
        # Qubits
        qubits = self.prepare_qubits(key_alice)
        
        # Informações para Bob
        bases_bob = super().generate_bases(nqubits)
        
        # Enviando os qubits
        bob_received_qubits, interference_qubits = self.network.send_qubits(route, qubits)
        
        # Bob mede os qubits
        key_bob = self.apply_measurement(bob_received_qubits, bases_bob)
        
        # Qubits sem interferência
        shared_key = super.check_key(key_bob, key_alice)
        
        # Resultados da execução
        self.generated_key = key_alice
        self.shared_key = shared_key
        self.different_bits = len(key_alice) - len(shared_key)
        self.key_sucess = len(shared_key) / nqubits