from pathlib import Path


class ForgeRegistryGenerator:

    @staticmethod
    def ensure_modblocks_file(fs_gateway):

        path = Path(fs_gateway.root) / \
            "src/main/java/com/example/mod/registry/ModBlocks.java"

        if path.exists():
            return

        path.parent.mkdir(parents=True, exist_ok=True)

        base_content = """
package com.example.mod.registry;

import net.minecraft.world.level.block.Block;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;

public class ModBlocks {

    public static final DeferredRegister<Block> BLOCKS =
        DeferredRegister.create(ForgeRegistries.BLOCKS, "mod");

    public static void register() {
        BLOCKS.register(FMLJavaModLoadingContext.get().getModEventBus());
    }
}
""".strip()

        with open(path, "w", encoding="utf-8") as f:
            f.write(base_content)

    # ----------------------------------------------------

    @staticmethod
    def add_block_registration(fs_gateway, name: str):

        path = Path(fs_gateway.root) / \
            "src/main/java/com/example/mod/registry/ModBlocks.java"

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        constant_name = name.upper()
        class_name = name.title().replace("_", "")

        registration_line = f"""
    public static final RegistryObject<Block> {constant_name} =
        BLOCKS.register("{name}", {class_name}::new);
""".strip()

        if constant_name in content:
            return  # already registered

        # Insert before closing brace
        content = content.replace(
            "public class ModBlocks {",
            f"public class ModBlocks {{\n\n{registration_line}\n"
        )

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)