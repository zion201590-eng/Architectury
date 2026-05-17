import pytest
from xengine.domain.project_model import ProjectModel
from xengine.core.engine import Engine


def test_preview_does_not_apply():
    project = ProjectModel("TestMod")
    engine = Engine(project)

    engine.preview("add ruby block")

    assert not project.has_entry("ruby_block")


def test_confirm_applies_changes():
    project = ProjectModel("TestMod")
    engine = Engine(project)

    engine.preview("add ruby block")
    engine.confirm()

    assert project.has_entry("ruby_block")


def test_confirm_without_preview_fails():
    project = ProjectModel("TestMod")
    engine = Engine(project)

    with pytest.raises(ValueError):
        engine.confirm()