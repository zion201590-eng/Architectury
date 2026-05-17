from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QFont


class MainMenu(QWidget):

    def __init__(self, on_chat, on_generate):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(20)

        title = QLabel("MAIN MENU")
        title.setFont(QFont("Arial", 24))
        title.setStyleSheet("color: white;")

        btn_chat = QPushButton("AI CHAT")
        btn_generate = QPushButton("GENERATE MDK")

        btn_chat.clicked.connect(on_chat)
        btn_generate.clicked.connect(on_generate)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(btn_chat)
        layout.addWidget(btn_generate)
        layout.addStretch()

        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget { background-color: #111; color: white; }
            QPushButton {
                background-color: #222;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #333;
            }
        """)