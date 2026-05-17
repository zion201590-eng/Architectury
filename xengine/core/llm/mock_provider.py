import json
from xengine.core.llm.provider_base import LLMProvider


class MockProvider(LLMProvider):

    def generate(self, prompt: str) -> str:
        # Simulated LLM returning JSON string
        response = {
            "changes": [
                {
                    "type": "add_block",
                    "name": "ruby_block"
                }
            ]
        }
        return json.dumps(response)