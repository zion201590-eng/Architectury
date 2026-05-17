from dataclasses import dataclass


@dataclass
class AIConfig:
    model: str = "llama3"
    temperature: float = 0.7
    context_size: int = 8192
    max_tokens: int = 2048


@dataclass
class MDKConfig:
    mod_name: str = ""
    mod_id: str = ""
    author: str = ""
    version: str = "1.0.0"
    minecraft_version: str = "1.20.1"
    platform: str = "Forge"
    forge_version: str = "47.2.0"


class AppState:

    def __init__(self):
        self.ai_config = AIConfig()
        self.mdk_config = MDKConfig()
        self.project_root = None