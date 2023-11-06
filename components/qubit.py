from random import randint

class Qubit():
    """
    Um objeto para abstrair um bit quântico.
    Notas:
        O qubit pode estar entrelaçado ou nos estados |0> ou |1>;
        Ao iniciar um qubit, seu estado é |0>.
    """
    
    def __init__(self) -> None:
        self.lastState = 0
        self.lastResult = None
        self.superposition = False
    
    def status(self):
        lastState = f"Último estado do qubit: {self.lastState}"
        lastResult = f"lastResult de sua medição: {self.lastResult}"
        superposition = f"O qubit está em superposição: {self.superposition}"
        print(lastState, lastResult, superposition, sep="\n")
        
    def X(self):
        """
        Faz um bitflip. Se o estado estiver em 0, vai para 1 e visse-versa.
        """
        
        if self.lastState == 0:
            self.lastState = 1
        else:
            self.lastState = 0
    
    def H(self):
        """
        Coloca um qubit em estado de Bell (superposição). O lastResult de sua medição é aleatório.
        """
        
        if self.superposition:
            self.superposition = False
        else:
            self.superposition = True
        
    def interference(self):
        """
        Simula uma pequena interferência no qubit. Faz um bit flip com um XOR.
        """
        
        self.lastState ^=  1
        
    def measure(self):
        """
        Mede o estado de um qubit.
        returns:
            collapse (int): lastResult de uma medição (0 ou 1).
        """
        
        # Se o qubit estiver em superposição, tira ele desse estado e escolhe um valor aleatório 0 ou 1 para colapsar no seu lastResult
        if self.superposition:
            self.superposition = False
            collapse = randint(0, 1)
            self.lastResult = collapse
        # Se o qubit não estiver em superposição, colapsa no último valor registrado
        else:
            collapse = self.lastState
            self.lastResult = self.lastState
        return collapse

