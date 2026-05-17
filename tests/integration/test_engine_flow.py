from xengine.domain.project_model import ProjectModel
from xengine.core.engine import Engine


def test_engine_add_block_preview():
    project = ProjectModel("TestMod")
    engine = Engine(project)

    changes = engine.preview("add ruby block")

    assert not project.has_entry("ruby_block")
    assert len(changes) == 1


def test_engine_add_block_confirm():
    project = ProjectModel("TestMod")
    engine = Engine(project)

    engine.preview("add ruby block")
    engine.confirm()

    assert project.has_entry("ruby_block")