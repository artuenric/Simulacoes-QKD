from .qubit import Qubit
print("Importando Epr")
class Epr():
    """
    Um objeto que simula dois qubits em estado de Bell.
    """
    def __init__(self) -> None:
        self.qubit1 = Qubit()
        self.qubit2 = Qubit()

    def H(self):
        self.qubit1.H()
        self.qubit2.H()
    
    def X(self):
        self.qubit1.X()
        self.qubit2.X()
        
    def getQubits(self):
        return self.qubit1, self.qubit2

