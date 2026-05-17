import tempfile
from pathlib import Path

from xengine.domain.project_model import ProjectModel
from xengine.core.engine import Engine


def test_main_mod_class_generated():

    with tempfile.TemporaryDirectory() as tmpdir:

        project = ProjectModel("TestMod")

        engine = Engine(
            project_model=project,
            project_root=tmpdir
        )

        engine.preview("add ruby block")
        engine.confirm()

        main_path = Path(tmpdir) / \
            "src/main/java/com/example/mod/ModMain.java"

        assert main_path.exists()

        content = main_path.read_text()

        assert "ModBlocks.register();" in content