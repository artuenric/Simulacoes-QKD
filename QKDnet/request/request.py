# App pode ser o próprio protocolo, ao invés de só uma string
from ..protocols import *

class Request:
    """
    Um objeto para ser usado como requisição de chave quântica.
    """
    
    def __init__(self, num_id, classe, app, priority, alice, bob):
        self.num_id = num_id
        self.classe = classe
        self.min_fidelity = None
        self.keys_need = None
        self.set_keys_need()
        self.app = app
        self.protocol = None
        self.set_protocol(app)
        self.priority = priority
        self.alice = alice
        self.bob = bob
        self.route = []
        self.esttimeted_time = None
        self.current_time = 0
        self.max_time = None
        self.served = False
        
        
    def __str__(self) -> str:
        return f"{self.app}: {self.alice}-{self.bob} (P:{self.priority} Key: {self.keys_need})"
    
    def set_protocol(self, app):
        """
        Define o protocolo em uso de acordo com a app.

        Args:
            app (string): Nome da app (BB84, E91 ou B92)
        """

        if app == "BB84":
            self.protocol = BB84()
        elif app == "E91":
            self.protocol = E91()
        elif app == "B92":
            self.protocol = B92()
    
    def set_keys_need(self):
        """
        Define o número de chaves que a requisição precisa.
        """
        if self.classe == "Class A":
            self.keys_need = 100
        elif self.classe == "Class B":
            self.keys_need = 250
        elif self.classe == "Class C":
            self.keys_need = 500
        elif self.classe == "Class D":
            self.keys_need = 1000
        elif self.classe == "Class E":
            self.keys_need = 1500
    
    def set_estimated_time(self, time):
        """
        Define o tempo estimado (em time slot) para o request ser atendido.
        """
        self.estimated_time = time
    
    def set_max_time(self):
        """
        Define o tempo máximo (em time slot) para o request ser atendido.
        """
        # Precisa de um polimorfismo aqui. Talvez role um de sobrecarga.
        pass
    
    def get_info(self):
        """
        Retorna informações sobre a requisição.
        """
        return {
            "Num ID": self.num_id,
            "Priority": self.priority,
            "Keys Need": self.keys_need,
            "Alice e Bob": f"{self.alice}-{self.bob}",
            "App": self.app
        }
    
    def update_keys(self, keys):
        """
        Atualiza o número de chaves que a requisição precisa.
        Args:
            keys (int): Tamanho da chave obtida durante a execução do protocolo.
        """
        self.keys_need -= keys
        
        # Subtrai do valor de chaves necessárias o número obtido da última execução do protocolo.
        # *self.keys_need -= self.protocol.shared_key