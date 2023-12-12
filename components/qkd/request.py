class Request:
    """
    Um objeto para ser usado como requisição de chave quântica.
    """
    
    def __init__(self, app, alice, bob, priority):
        self.app = app
        self.alice = alice
        self.bob = bob
        self.priority = priority
        self.chaves = 100
        self.route = []
        
    def __str__(self) -> str:
        return f"{self.app}: {self.alice}-{self.bob} (P:{self.priority} Key: {self.chaves})"
    
    def obter_chaves(self, chaves):
        """
        Atualiza o número de chaves que a requisição precisa.
        Args:
            chaves (int): Tamanho da chave obtida durante a execução do protocolo.
        """
        self.chaves -= chaves
        
