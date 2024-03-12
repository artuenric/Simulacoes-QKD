import numpy as np

class DataCenter():
    def __init__(self, data):
        self.all_received_requests = []
        self.served_requests = []
        self.fail_requests = []
        self.key_sucess_rates = []
        self.throughput = 0
        self.final_time = 0

    def get_throughput(self):
        """
        Calcula a taxa de sucesso das requisições.
        """
        self.throughput = len(self.served_requests) / len(self.all_received_requests)
        return self.throughput

    def get_key_sucess_rate(self):
        """
        Calcula a taxa de sucesso das chaves.
        """
        self.key_sucess_rates = np.mean(self.key_sucess_rates)
        return self.key_sucess_rates