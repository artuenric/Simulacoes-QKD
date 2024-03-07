from QKDnet.protocols import BB84
from components import Network, Controller

# Classe abstrata e herança
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
        self.nome = 'ai'
    def testante(self):
        print("Oba testo")

a = Computado()
a.nome = 'oi'
b = Computado()
lista = [a, b]

lista_copia = lista.copy()
lista_copia[0].nome = 'tchau'

print(lista[0].nome)
print(lista_copia[0].nome)