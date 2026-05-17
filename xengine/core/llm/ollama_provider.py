import requests
import json


class OllamaProvider:

    def __init__(
        self,
        model: str = "llama2:latest",
        base_url: str = "http://127.0.0.1:11434",
        timeout: int = 120,
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate_stream(self, prompt: str):

        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True
        }

        with requests.post(
            url,
            json=payload,
            stream=True,
            timeout=self.timeout,
        ) as response:

            response.raise_for_status()

            for line in response.iter_lines():

                if not line:
                    continue

                data = json.loads(line.decode("utf-8"))

                if "response" in data:
                    yield data["response"]

                if data.get("done"):
                    break