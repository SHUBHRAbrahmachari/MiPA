from abc import ABC, abstractmethod


class CheckpointerFactory(ABC):
    @abstractmethod
    def load_checkpointer(self):
        pass
