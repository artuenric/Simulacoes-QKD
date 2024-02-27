from ..quantum import Epr
from .protocol import Protocol

class E91(Protocol):
    def __init__(self, network):
        super().__init__()
        super().network = network
        super().app = "E91"
        
    def prepare_qubits(self, key, bases):
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
    
    def apply_measurement(self, qubits, bases):
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
    
    
    def run(self, route):
        """
        Executa o protocolo QKD E91.

        Args:
            # network (Network): Rede em que o protocolo será executado.
            route (lista): Rota de Alice para Bob.

        Returns:
            Dict : Dicionário de dicionários com as informações das execuções.
        """
        # Número de qubits para geração da chave
        nqubits = super().network.nqubits
        
        # Informações para Alice
        key_alice = super().create_key(nqubits)
        bases_alice = super().generate_bases(nqubits)
        
        # Eprs
        pairs = self.prepare_qubits(key_alice, bases_alice)
        
        # Informações para Bob
        bases_bob = super().generate_bases(nqubits)
        
        # Enviando os qubits
        received_qubits, interference_qubits = super().network.send_eprs(route, pairs)
        
        # Bob medindo os qubits
        measured_qubits = self.aplly_measurement(received_qubits, bases_bob)
        
        # Comparando as bases de Alice e Bob
        matching_bases = self.compare_bases(bases_alice, bases_bob)
        
        # Chave obtida de acordo com as bases
        key_bob = super().get_key(measured_qubits, matching_bases)
        
        # Chave obtida de acordo com as bases
        key_bob = super().get_key(measured_qubits, matching_bases)
        
        # Checando chave
        shared_key = super().check_key(key_bob, key_alice)
        
        # Resultados da execução
        super().generated_key = key_alice
        super().shared_key = shared_key
        super().different_bits = len(key_alice) - len(shared_key)
        super().key_sucess = len(shared_key) / nqubits
        
        results = dict()
        results['app'] = 'E91'
        results['generated key'] = key_alice
        results['shared key'] = shared_key
        results['different bits'] = len(key_alice) - len(shared_key)
        results['key sucess'] = len(shared_key) / nqubits
        