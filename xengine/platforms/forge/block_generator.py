class ForgeBlockGenerator:

    @staticmethod
    def class_name(name: str) -> str:
        return name.title().replace("_", "")

    @staticmethod
    def generate_block_class(name: str) -> str:
        class_name = ForgeBlockGenerator.class_name(name)

        return f"""
package com.example.mod.block;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;

public class {class_name} extends Block {{

    public {class_name}() {{
        super(BlockBehaviour.Properties.of());
    }}
}}
""".strip()

    @staticmethod
    def generate_blockstate_json(name: str) -> str:
        return f"""
{{
  "variants": {{
    "": {{ "model": "mod:block/{name}" }}
  }}
}}
""".strip()

    @staticmethod
    def generate_block_model_json(name: str) -> str:
        return f"""
{{
  "parent": "block/cube_all",
  "textures": {{
    "all": "mod:block/{name}"
  }}
}}
""".strip()

    @staticmethod
    def generate_item_model_json(name: str) -> str:
        return f"""
{{
  "parent": "mod:block/{name}"
}}
""".strip()

    @staticmethod
    def generate_lang_entry(name: str) -> tuple[str, str]:
        readable = name.replace("_", " ").title()
        key = f"block.mod.{name}"
        return key, readable