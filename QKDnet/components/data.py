import numpy as np

class DataBase():
    """
    Armazena os dados coletados no controlador.
    """
    def __init__(self):
        self.all_requests = []
        self.served_requests = []
        self.failed_requests = []
        self.key_sucess_rates = []
        self.key_sucess_rate = 0
        self.throughput = 0
        self.final_time = 0

    def get_throughput(self):
        """
        Calcula a taxa de sucesso das requisições.
        """
        self.throughput = len(self.served_requests) / len(self.all_requests)
        return self.throughput
    
    def get_key_sucess_rate(self):
        """
        Calcula a taxa de sucesso das chaves.
        """
        self.key_sucess_rate = np.mean(self.key_sucess_rates)
        return self.key_sucess_rate
    
    def collect_protocol_data(self, protocol):
        """
        Coleta os dados das requisições atendidas.
        
        Args:
            protocol (Protocol): Protocolo de QKD.
        """
        self.key_sucess_rates.append(protocol.sucess_rate)
    
    def collect_served_requests_data(self, request):
        """
        Coleta as requisições atendidas.
        """
        self.served_requests.append(request)
    
    def collect_failed_requests_data(self, request):
        """
        Coleta as requisições não atendidas.
        """
        self.failed_requests.append(request)
    
    def collect_all_requests_data(self, requests):
        """
        Coleta todas as requisições.
        """
        self.all_requests.extend(requests)
    
    def clear_data(self):
        """
        Limpa os dados coletados.
        """
        self.all_requests.clear()
        self.served_requests.clear()
        self.failed_requests.clear()
        self.key_sucess_rates.clear()
        self.throughput = 0
        self.final_time = 0