import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit,
    QLineEdit, QPushButton, QHBoxLayout,
    QSplitter, QTreeView, QApplication
)

from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import Qt


class AIChatWindow(QWidget):

    def __init__(self, ai_bridge, on_back):
        super().__init__()

        self.ai = ai_bridge

        main_layout = QVBoxLayout()

        # -------------------------------------------------
        # SPLITTER (Left Tree | Center Chat | Right Logs)
        # -------------------------------------------------

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # ---------- LEFT: FILE TREE ----------
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath("")

        self.file_tree = QTreeView()
        self.file_tree.setModel(self.file_model)
        self.file_tree.setHeaderHidden(True)

        splitter.addWidget(self.file_tree)

        # ---------- CENTER: CHAT ----------
        center_widget = QWidget()
        center_layout = QVBoxLayout()

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        self.input = QLineEdit()

        btn_send = QPushButton("Send")
        btn_confirm = QPushButton("Confirm")
        btn_undo = QPushButton("Undo")
        btn_back = QPushButton("Back")

        btn_send.clicked.connect(self.send_message)
        btn_confirm.clicked.connect(self.confirm)
        btn_undo.clicked.connect(self.undo)
        btn_back.clicked.connect(on_back)

        bottom = QHBoxLayout()
        bottom.addWidget(self.input)
        bottom.addWidget(btn_send)
        bottom.addWidget(btn_confirm)
        bottom.addWidget(btn_undo)
        bottom.addWidget(btn_back)

        center_layout.addWidget(self.chat)
        center_layout.addLayout(bottom)

        center_widget.setLayout(center_layout)

        splitter.addWidget(center_widget)

        # ---------- RIGHT: PREVIEW / LOG ----------
        self.log_panel = QTextEdit()
        self.log_panel.setReadOnly(True)

        splitter.addWidget(self.log_panel)

        splitter.setSizes([250, 600, 250])

        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

    # -------------------------------------------------

    def set_project_root(self, path):

        if not path:
            return

        abs_path = os.path.abspath(path)

        self.file_model.setRootPath(abs_path)
        self.file_tree.setRootIndex(
            self.file_model.index(abs_path)
        )

    # -------------------------------------------------

    def send_message(self):

        text = self.input.text()
        if not text:
            return

        self.chat.append(f"YOU: {text}")
        self.input.clear()

        result = self.ai.process(text)

        if result["type"] == "chat_stream":

            self.chat.append("AI: ")
            QApplication.processEvents()

            for chunk in self.ai.ai.stream_chat(text):
                self.chat.insertPlainText(chunk)
                QApplication.processEvents()

            return

        if result["type"] == "auto_confirm":
            self.log_panel.append("[AUTO APPLIED]")
            self.log_panel.append(str(result["changes"]))
            self.refresh_tree()
            return

        if result["type"] == "engineering_preview":
            self.log_panel.append("[PREVIEW]")
            self.log_panel.append(str(result["changes"]))
            return

        if result["type"] == "error":
            self.chat.append(result["message"])
            return

    # -------------------------------------------------

    def confirm(self):
        result = self.ai.confirm()
        self.log_panel.append(str(result))
        self.refresh_tree()

    def undo(self):
        result = self.ai.undo()
        self.log_panel.append(str(result))
        self.refresh_tree()

    # -------------------------------------------------

    def refresh_tree(self):
        root = self.file_model.rootPath()
        self.file_model.setRootPath("")
        self.file_model.setRootPath(root)