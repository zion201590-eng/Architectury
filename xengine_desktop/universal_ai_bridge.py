from xengine.universal_ai import UniversalAI


class UniversalAIBridge:

    def __init__(self, app_state):
        self.state = app_state
        self.ai = None

    # -----------------------------------------------------

    def init_ai(self):
        if not self.state.project_root:
            return

        self.ai = UniversalAI(
            project_root=self.state.project_root
        )

    # -----------------------------------------------------

    def process(self, message: str):

        if not self.ai:
            return {
                "type": "error",
                "message": "No project selected. Create MDK first."
            }

        return self.ai.process(message)

    def stream_chat(self, message: str):

        if not self.ai:
            yield "[ERROR]: No project selected."
            return

        yield from self.ai.stream_chat(message)

    def confirm(self):
        if self.ai:
            return self.ai.confirm()

    def undo(self):
        if self.ai:
            return self.ai.undo()