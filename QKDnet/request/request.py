# App pode ser o próprio protocolo, ao invés de só uma string
from ..protocols import *

class Request:
    """
    Um objeto para ser usado como requisição de chave quântica.
    """
    
    def __init__(self, num_id, category, app, priority, alice, bob):
        # Identificação
        self.num_id = num_id
        self.category = category
        self.min_fidelity = None
        self.keys_need = None
        self.set_keys_need()
        self.app = app
        self.protocol = None
        self.set_protocol(app)
        self.priority = priority
        # Rota
        self.alice = alice
        self.bob = bob
        self.route = []
        self.route_length = None
        # Tempo
        self.esttimeted_time = None
        self.time_left = None
        self.max_start_time = None
        self.max_time = None
        self.set_max_time()
        # Status
        self.served = False
        self.finished = False
        
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
        if self.category == "Class A":
            self.keys_need = 100
        elif self.category == "Class B":
            self.keys_need = 250
        elif self.category == "Class C":
            self.keys_need = 500
        elif self.category == "Class D":
            self.keys_need = 1000
        elif self.category == "Class E":
            self.keys_need = 1500
    
    def set_route(self, route):
        """
        Define a rota para a requisição.
        """
        self.route = route
        self.route_length = len(self.route)
    
    def set_times(self, time):
        """
        Define os tempos (em time slot) para a requisição.
        """
        # Define o tempo estimado para ser atendido
        self.estimated_time = time
        # Define o tempo máximo para o início do atendimento
        self.max_start_time = self.max_time - self.estimated_time
    
    def set_max_time(self):
        """
        Define o tempo máximo (em time slot) para o request ser atendido.
        """
        # Define o tempo máximo para ser atendido
        # (self.keys_need // self.protocol.sucess_rate)
        self.max_time = 100 
        # Define o tempo restante para ser atendido
        self.time_left = self.max_time
    
    def get_info(self):
        """
        Retorna informações sobre a requisição.
        """
        return {
            "Num ID": self.num_id,
            "App": self.app,
            "Priority": self.priority,
            "Keys Need": self.keys_need,
            "Alice e Bob": f"{self.alice}-{self.bob}",
        }
    
    def update_keys(self, keys):
        """
        Atualiza o número de chaves que a requisição precisa.
        Args:
            keys (int): Tamanho da chave obtida durante a execução do protocolo.
        """
        self.keys_need -= keys
        
    def update_time(self):
        """
        Atualiza o tempo de atendimento para a requisição.
        """
        self.time_left = self.time_left - 1 if self.time_left > 0 else 0