class Request:
    """
    Um objeto para ser usado como requisição de chave quântica.
    """
    
    def __init__(self, classe, app, priority, alice, bob):
        self.classe = classe
        self.app = app
        self.priority = priority
        self.keys
        self.set_keys()
        self.alice = alice
        self.bob = bob
        self.route = []
        
    def __str__(self) -> str:
        return f"{self.app}: {self.alice}-{self.bob} (P:{self.priority} Key: {self.keys})"
    
    def set_keys(self):
        """
        Define o número de chaves que a requisição precisa.
        """
        if self.classe == "Class A":
            self.keys = 100
        elif self.classe == "Class B":
            self.keys = 250
        elif self.classe == "Class C":
            self.keys = 500
        elif self.classe == "Class D":
            self.keys = 1000
        elif self.classe == "Class E":
            self.keys = 1500
    
    def update_keys(self, keys):
        """
        Atualiza o número de chaves que a requisição precisa.
        Args:
            keys (int): Tamanho da chave obtida durante a execução do protocolo.
        """
        self.keys -= keys
        
