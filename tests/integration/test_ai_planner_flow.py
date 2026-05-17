from xengine.domain.project_model import ProjectModel
from xengine.core.engine import Engine


def test_ai_planner_add_block_flow():
    project = ProjectModel("TestMod")
    engine = Engine(project)

    engine.preview("please add ruby block")
    engine.confirm()

    assert project.has_entry("ruby_block")