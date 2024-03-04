from .protocol import Protocol
from ..quantum import Qubit

class BB84(Protocol):
    """
    Protocolo QKD BB84.
    """
    def __init__(self):
        super().__init__()
        self.app = "BB84"
        self.sucess_rate = 0.5

    
    def prepare_qubits(self, key, bases):
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
    
    def apply_measurement(self, qubits, bases):
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
    
    def run(self, network, route):
        """
        Executa o protocolo QKD BB84.

        Args:
            network (Network): Rede em que o protocolo será executado.

        Returns:
            Dict : Dicionário de dicionários com as informações das execuções.
        """
        # Número de qubits para geração da chave
        nqubits = network.nqubits
        
        # Informações para Alice
        key_alice = super().create_key(nqubits)
        
        bases_alice = super().generate_bases(nqubits)
        
        # Qubits
        qubits = self.prepare_qubits(key_alice, bases_alice)
        
        # Informações para Bob
        bases_bob = super().generate_bases(nqubits)
        
        # Enviando os qubits
        received_qubits, interference_qubits = network.send_qubits(route, qubits)
        
        # Bob mede os qubits
        measured_qubits = self.apply_measurement(received_qubits, bases_bob)
        
        # Comparando as bases de Alice e Bob
        matching_bases = super().compare_bases(bases_alice, bases_bob)
        
        # Chave obtida de acordo com as bases
        key_bob = super().get_key(measured_qubits, matching_bases)
        
        # Checando a chave
        shared_key = super().check_key(key_bob, key_alice)

        # Resultados da execução
        self.generated_key = key_alice
        self.shared_key = shared_key
        self.different_bits = len(key_alice) - len(shared_key)
        self.key_sucess = len(shared_key) / nqubits