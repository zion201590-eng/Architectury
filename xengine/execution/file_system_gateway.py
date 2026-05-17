from pathlib import Path


class FileSystemGateway:

    def __init__(self, root_path: str):
        self.root = Path(root_path)

    def write_file(self, relative_path: str, content: str):
        file_path = self.root / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    def file_exists(self, relative_path: str) -> bool:
        return (self.root / relative_path).exists()