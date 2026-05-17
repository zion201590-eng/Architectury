import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox
)


class GenerateMDKWindow(QWidget):

    def __init__(self, state, on_back):
        super().__init__()

        self.state = state
        self.on_back = on_back

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Mod Name"))
        self.mod_name = QLineEdit()

        layout.addWidget(QLabel("Mod ID"))
        self.mod_id = QLineEdit()

        layout.addWidget(QLabel("Author"))
        self.author = QLineEdit()

        layout.addWidget(QLabel("Minecraft Version"))
        self.mc_version = QComboBox()
        self.mc_version.addItems(["1.20.1", "1.19.2"])

        layout.addWidget(QLabel("Platform"))
        self.platform = QComboBox()
        self.platform.addItems(["Forge", "Fabric"])

        btn_generate = QPushButton("Generate Project")
        btn_back = QPushButton("Back")

        btn_generate.clicked.connect(self.generate)
        btn_back.clicked.connect(self.on_back)

        layout.addWidget(self.mod_name)
        layout.addWidget(self.mod_id)
        layout.addWidget(self.author)
        layout.addWidget(self.mc_version)
        layout.addWidget(self.platform)
        layout.addWidget(btn_generate)
        layout.addWidget(btn_back)

        self.setLayout(layout)

    # -----------------------------------------------------

    def generate(self):

        mod_id = self.mod_id.text().strip()

        if not mod_id:
            return

        project_path = os.path.join("projects", mod_id)

        os.makedirs(project_path, exist_ok=True)

        self.state.project_root = project_path

        # ✅ Инициализируем AI после создания проекта
        from xengine_desktop.main import DesktopApp
        DesktopApp.instance.ai_bridge.init_ai()

        print("✅ Project created at:", project_path)