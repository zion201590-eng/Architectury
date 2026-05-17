from xengine.platforms.base.adapter import PlatformAdapter


class FabricAdapter(PlatformAdapter):

    def add_block(self, project_model, name: str):
        # Simulate Fabric-specific registry behavior
        project_model.registry.add_entry(name, "fabric_block")

    def add_item(self, project_model, name: str):
        project_model.registry.add_entry(name, "fabric_item")