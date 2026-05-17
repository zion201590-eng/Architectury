from xengine.domain.project_model import ProjectModel
from xengine.core.engine import Engine


def test_llm_provider_pipeline():
    project = ProjectModel("TestMod")
    engine = Engine(project)

    engine.preview("please create ruby block")
    engine.confirm()

    assert project.has_entry("ruby_block")