from pathlib import Path


class ForgeMainModGenerator:

    @staticmethod
    def ensure_main_class(fs_gateway):

        path = Path(fs_gateway.root) / \
            "src/main/java/com/example/mod/ModMain.java"

        if path.exists():
            return

        path.parent.mkdir(parents=True, exist_ok=True)

        base_content = """
package com.example.mod;

import net.minecraftforge.fml.common.Mod;
import com.example.mod.registry.ModBlocks;

@Mod("mod")
public class ModMain {

    public ModMain() {
        ModBlocks.register();
    }
}
""".strip()

        with open(path, "w", encoding="utf-8") as f:
            f.write(base_content)

    # ----------------------------------------------------

    @staticmethod
    def ensure_register_call(fs_gateway):

        path = Path(fs_gateway.root) / \
            "src/main/java/com/example/mod/ModMain.java"

        if not path.exists():
            return

        content = path.read_text()

        if "ModBlocks.register();" in content:
            return

        content = content.replace(
            "public ModMain() {",
            "public ModMain() {\n        ModBlocks.register();"
        )

        path.write_text(content)