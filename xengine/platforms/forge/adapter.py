import json
from pathlib import Path

from xengine.platforms.base.adapter import PlatformAdapter
from xengine.platforms.forge.block_generator import ForgeBlockGenerator
from xengine.platforms.forge.registry_generator import ForgeRegistryGenerator
from xengine.platforms.forge.mod_main_generator import ForgeMainModGenerator


class ForgeAdapter(PlatformAdapter):

    # =====================================================
    # DOMAIN OPERATIONS
    # =====================================================

    def add_block(self, project_model, name: str):
        project_model.registry.add_entry(name, "block")

    def add_item(self, project_model, name: str):
        project_model.registry.add_entry(name, "item")

    # =====================================================
    # FILE GENERATION
    # =====================================================

    def generate_block_files(self, fs_gateway, name: str):

        class_name = ForgeBlockGenerator.class_name(name)

        # -------------------------------------------------
        # 1️⃣ Java block class
        # -------------------------------------------------

        fs_gateway.write_file(
            f"src/main/java/com/example/mod/block/{class_name}.java",
            ForgeBlockGenerator.generate_block_class(name)
        )

        # -------------------------------------------------
        # 2️⃣ blockstate JSON
        # -------------------------------------------------

        fs_gateway.write_file(
            f"src/main/resources/assets/mod/blockstates/{name}.json",
            ForgeBlockGenerator.generate_blockstate_json(name)
        )

        # -------------------------------------------------
        # 3️⃣ block model JSON
        # -------------------------------------------------

        fs_gateway.write_file(
            f"src/main/resources/assets/mod/models/block/{name}.json",
            ForgeBlockGenerator.generate_block_model_json(name)
        )

        # -------------------------------------------------
        # 4️⃣ item model JSON
        # -------------------------------------------------

        fs_gateway.write_file(
            f"src/main/resources/assets/mod/models/item/{name}.json",
            ForgeBlockGenerator.generate_item_model_json(name)
        )

        # -------------------------------------------------
        # 5️⃣ Lang file update
        # -------------------------------------------------

        lang_path = Path(fs_gateway.root) / \
            "src/main/resources/assets/mod/lang/en_us.json"

        key, value = ForgeBlockGenerator.generate_lang_entry(name)

        lang_data = {}

        if lang_path.exists():
            try:
                with open(lang_path, "r", encoding="utf-8") as f:
                    lang_data = json.load(f)
            except json.JSONDecodeError:
                lang_data = {}

        lang_data[key] = value

        lang_path.parent.mkdir(parents=True, exist_ok=True)

        with open(lang_path, "w", encoding="utf-8") as f:
            json.dump(lang_data, f, indent=2)

        # -------------------------------------------------
        # 6️⃣ Registry generation (ModBlocks.java)
        # -------------------------------------------------

        ForgeRegistryGenerator.ensure_modblocks_file(fs_gateway)
        ForgeRegistryGenerator.add_block_registration(fs_gateway, name)

        # -------------------------------------------------
        # 7️⃣ Main mod class generation + register() call
        # -------------------------------------------------

        ForgeMainModGenerator.ensure_main_class(fs_gateway)
        ForgeMainModGenerator.ensure_register_call(fs_gateway)