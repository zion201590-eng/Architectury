import tempfile
from pathlib import Path

from xengine.domain.project_model import ProjectModel
from xengine.core.engine import Engine


def test_block_file_is_generated():

    with tempfile.TemporaryDirectory() as tmpdir:

        project = ProjectModel("TestMod")

        engine = Engine(
            project_model=project,
            project_root=tmpdir
        )

        engine.preview("add ruby block")
        engine.confirm()

        expected_path = Path(tmpdir) / \
            "src/main/java/com/example/mod/block/RubyBlock.java"

        assert expected_path.exists()