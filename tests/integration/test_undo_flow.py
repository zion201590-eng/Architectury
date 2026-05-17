import pytest
from xengine.domain.project_model import ProjectModel
from xengine.core.engine import Engine


def test_undo_reverts_changes():
    project = ProjectModel("TestMod")
    engine = Engine(project)

    engine.preview("add ruby block")
    engine.confirm()

    assert project.has_entry("ruby_block")

    engine.undo()

    assert not project.has_entry("ruby_block")


def test_undo_without_history_fails():
    project = ProjectModel("TestMod")
    engine = Engine(project)

    with pytest.raises(ValueError):
        engine.undo()