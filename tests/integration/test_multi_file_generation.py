import tempfile
from pathlib import Path

from xengine.domain.project_model import ProjectModel
from xengine.core.engine import Engine


def test_multi_file_block_generation():

    with tempfile.TemporaryDirectory() as tmpdir:

        project = ProjectModel("TestMod")

        engine = Engine(
            project_model=project,
            project_root=tmpdir
        )

        engine.preview("add ruby block")
        engine.confirm()

        root = Path(tmpdir)

        assert (root / "src/main/java/com/example/mod/block/RubyBlock.java").exists()
        assert (root / "src/main/resources/assets/mod/blockstates/ruby_block.json").exists()
        assert (root / "src/main/resources/assets/mod/models/block/ruby_block.json").exists()
        assert (root / "src/main/resources/assets/mod/models/item/ruby_block.json").exists()
        assert (root / "src/main/resources/assets/mod/lang/en_us.json").exists()