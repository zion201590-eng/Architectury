from xengine.core.engine import Engine
from xengine.domain.project_model import ProjectModel
from xengine.core.llm.ollama_provider import OllamaProvider


class UniversalAI:

    def __init__(self, project_root=None):

        self.project = ProjectModel("DesktopMod")

        self.engine = Engine(
            project_model=self.project,
            llm_provider=OllamaProvider(model="llama2:latest"),
            project_root=project_root
        )

        self.chat_provider = OllamaProvider(model="llama2:latest")

    # -----------------------------------------------------

    def process(self, message: str):

        if self._is_engineering_intent(message):
            return self._handle_engineering(message)

        return {"type": "chat_stream"}

    # -----------------------------------------------------

    def stream_chat(self, message: str):

        try:
            for chunk in self.chat_provider.generate_stream(message):
                yield chunk
        except Exception as e:
            yield f"[ERROR]: {str(e)}"

    # -----------------------------------------------------

    def _is_engineering_intent(self, msg: str):

        keywords = [
            "add", "create", "generate",
            "block", "item", "class",
            "register", "mod"
        ]

        msg = msg.lower()

        return any(k in msg for k in keywords)

    # -----------------------------------------------------

    def _handle_engineering(self, message: str):

        try:
            changes = self.engine.preview(message)

            # ✅ Smart Mode:
            # если только 1 change → авто подтверждаем
            if len(changes) == 1:
                applied = self.engine.confirm()
                return {
                    "type": "auto_confirm",
                    "changes": [c.to_dict() for c in applied]
                }

            return {
                "type": "engineering_preview",
                "changes": [c.to_dict() for c in changes]
            }

        except Exception as e:
            return {
                "type": "error",
                "message": str(e)
            }

    # -----------------------------------------------------

    def confirm(self):
        try:
            changes = self.engine.confirm()
            return {
                "type": "engineering_confirm",
                "changes": [c.to_dict() for c in changes]
            }
        except Exception as e:
            return {
                "type": "error",
                "message": str(e)
            }

    def undo(self):
        try:
            self.engine.undo()
            return {"type": "undo_success"}
        except Exception as e:
            return {
                "type": "error",
                "message": str(e)
            }