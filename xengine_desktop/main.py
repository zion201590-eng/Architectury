import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget

from xengine_desktop.app_state import AppState
from xengine_desktop.universal_ai_bridge import UniversalAIBridge
from xengine_desktop.ui.splash import SplashScreen
from xengine_desktop.ui.main_menu import MainMenu
from xengine_desktop.ui.ai_chat import AIChatWindow
from xengine_desktop.ui.generate_mdk import GenerateMDKWindow


class DesktopApp:

    # ✅ Глобальный instance для доступа из других экранов
    instance = None

    def __init__(self):

        # ✅ сохраняем instance
        DesktopApp.instance = self

        self.qt_app = QApplication(sys.argv)

        # -------------------------------
        # GLOBAL STATE
        # -------------------------------

        self.state = AppState()
        self.ai_bridge = UniversalAIBridge(self.state)

        # -------------------------------
        # STACKED SCREENS
        # -------------------------------

        self.stack = QStackedWidget()

        self.splash = SplashScreen(self.go_to_menu)

        self.menu = MainMenu(
            on_chat=self.go_to_chat,
            on_generate=self.go_to_generate
        )

        self.chat = AIChatWindow(
            self.ai_bridge,
            on_back=self.go_to_menu
        )

        self.generate = GenerateMDKWindow(
            self.state,
            on_back=self.go_to_menu
        )

        self.stack.addWidget(self.splash)
        self.stack.addWidget(self.menu)
        self.stack.addWidget(self.chat)
        self.stack.addWidget(self.generate)

        self.stack.setCurrentWidget(self.splash)
        self.stack.resize(1200, 800)
        self.stack.show()

    # ---------------------------------
    # NAVIGATION
    # ---------------------------------

    def go_to_menu(self):
        self.stack.setCurrentWidget(self.menu)

    def go_to_chat(self):

        # ✅ Обновляем дерево проекта перед входом
        self.chat.set_project_root(self.state.project_root)

        self.stack.setCurrentWidget(self.chat)

    def go_to_generate(self):
        self.stack.setCurrentWidget(self.generate)

    # ---------------------------------

    def run(self):
        sys.exit(self.qt_app.exec())


if __name__ == "__main__":
    app = DesktopApp()
    app.run()