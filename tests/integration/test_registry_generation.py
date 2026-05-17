import tempfile
from pathlib import Path

from xengine.domain.project_model import ProjectModel
from xengine.core.engine import Engine


def test_modblocks_registry_is_generated():

    with tempfile.TemporaryDirectory() as tmpdir:

        project = ProjectModel("TestMod")

        engine = Engine(
            project_model=project,
            project_root=tmpdir
        )

        engine.preview("add ruby block")
        engine.confirm()

        registry_path = Path(tmpdir) / \
            "src/main/java/com/example/mod/registry/ModBlocks.java"

        assert registry_path.exists()

        content = registry_path.read_text()

        assert "RUBY_BLOCK" in content
        assert '"ruby_block"' in content