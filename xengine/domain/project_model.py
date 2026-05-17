from xengine.domain.graph.registry_graph import RegistryGraph


class ProjectModel:
    def __init__(self, name: str):
        self.name = name
        self.registry = RegistryGraph()

    def add_block(self, name: str) -> None:
        self.registry.add_entry(name, "block")

    def add_item(self, name: str) -> None:
        self.registry.add_entry(name, "item")

    def has_entry(self, name: str) -> bool:
        return self.registry.has_entry(name)