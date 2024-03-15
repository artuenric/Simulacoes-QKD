from abc import ABC, abstractmethod

class Sorter(ABC):
    def __init__(self):
        self.category = None

    @abstractmethod
    def sort(self):
        pass