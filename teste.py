from QKDnet.protocols import BB84
from components import Network, Controller

# Definindo rede e controlador
rede = Network()
rede.set_topology("China")
controlador = Controller(rede)

# Algumas propriedades da rede
rede.nqubits = 300
rede.neprs = 3
rede.set_fidelity(0.95)
protocolando = BB84(rede)

routes = controlador.calculate_shortest_routes(1, 3)
protocolando.run(routes[0])
print(protocolando.generated_key)

# Classe abstrata e herança
"""
from abc import ABC, abstractmethod
class Coisa(ABC):
    def __init__(self) -> None:
        print("Coisou")
    
    @abstractmethod
    def testante(self):
        pass
    
class Computado(Coisa):
    def __init__(self) -> None:
        super().__init__()

    def testante(self):
        print("Oba testo")

a = Computado()
a.testante()
"""