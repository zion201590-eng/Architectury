import pytest
from xengine.domain.project_model import ProjectModel


def test_add_block():
    project = ProjectModel("TestMod")
    project.add_block("ruby_block")

    assert project.has_entry("ruby_block")


def test_duplicate_block_raises():
    project = ProjectModel("TestMod")
    project.add_block("ruby_block")

    with pytest.raises(ValueError):
        project.add_block("ruby_block")