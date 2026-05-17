from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont


class SplashScreen(QWidget):

    def __init__(self, on_done):
        super().__init__()

        self.on_done = on_done

        layout = QVBoxLayout()
        layout.setSpacing(20)

        title = QLabel("XENGINE AI")
        title.setFont(QFont("Arial", 28))
        title.setStyleSheet("color: white;")
        title.setAlignment(
            title.alignment().AlignCenter
        )

        subtitle = QLabel("Loading AI Engine...")
        subtitle.setStyleSheet("color: gray;")
        subtitle.setAlignment(
            subtitle.alignment().AlignCenter
        )

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()

        self.setLayout(layout)
        self.setStyleSheet("background-color: #111;")

        QTimer.singleShot(2000, self.on_done)