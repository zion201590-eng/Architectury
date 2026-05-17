from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import uuid


class Change(ABC):

    def __init__(self):
        self.change_id = str(uuid.uuid4())

    @abstractmethod
    def apply(self, project_model, platform_adapter):
        pass

    @abstractmethod
    def rollback(self, project_model):
        pass

    @abstractmethod
    def explain(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass


@dataclass
class AddBlockChange(Change):
    name: str
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        super().__init__()

    def apply(self, project_model, platform_adapter):
        platform_adapter.add_block(project_model, self.name)

    def rollback(self, project_model):
        project_model.registry._entries.pop(self.name, None)

    def explain(self) -> str:
        return f"Add block '{self.name}' to registry."

    def to_dict(self) -> dict:
        return {
            "id": self.change_id,
            "type": "AddBlockChange",
            "name": self.name,
            "metadata": self.metadata,
        }


@dataclass
class AddItemChange(Change):
    name: str
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        super().__init__()

    def apply(self, project_model, platform_adapter):
        platform_adapter.add_item(project_model, self.name)

    def rollback(self, project_model):
        project_model.registry._entries.pop(self.name, None)

    def explain(self) -> str:
        return f"Add item '{self.name}' to registry."

    def to_dict(self) -> dict:
        return {
            "id": self.change_id,
            "type": "AddItemChange",
            "name": self.name,
            "metadata": self.metadata,
        }