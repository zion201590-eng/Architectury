from abc import ABC, abstractmethod


class PlatformAdapter(ABC):

    @abstractmethod
    def add_block(self, project_model, name: str):
        pass

    @abstractmethod
    def add_item(self, project_model, name: str):
        pass