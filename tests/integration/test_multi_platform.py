from xengine.domain.project_model import ProjectModel
from xengine.core.engine import Engine
from xengine.platforms.forge.adapter import ForgeAdapter
from xengine.platforms.fabric.adapter import FabricAdapter


def test_forge_adapter_registers_block_as_block():
    project = ProjectModel("TestMod")
    engine = Engine(project, platform_adapter=ForgeAdapter())

    engine.preview("add ruby block")
    engine.confirm()

    entry = project.registry.get_entry("ruby_block")
    assert entry.entry_type == "block"


def test_fabric_adapter_registers_block_as_fabric_block():
    project = ProjectModel("TestMod")
    engine = Engine(project, platform_adapter=FabricAdapter())

    engine.preview("add ruby block")
    engine.confirm()

    entry = project.registry.get_entry("ruby_block")
    assert entry.entry_type == "fabric_block"