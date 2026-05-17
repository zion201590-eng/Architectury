import json
import re
from jsonschema import validate, ValidationError

from xengine.core.schema import CHANGE_PLAN_SCHEMA
from xengine.core.llm.mock_provider import MockProvider
from xengine.domain.changes.change_plan import ChangePlan
from xengine.domain.changes.change_types import AddBlockChange, AddItemChange


class AIPlanner:

    def __init__(self, provider=None):
        self.provider = provider or MockProvider()

    # =====================================================
    # PUBLIC ENTRY
    # =====================================================

    def plan_from_user_input(self, user_input: str) -> ChangePlan:

        # MockProvider path (local deterministic logic)
        if isinstance(self.provider, MockProvider):
            name = self._extract_block_name(user_input)

            fake_json = {
                "changes": [
                    {
                        "type": "add_block",
                        "name": name
                    }
                ]
            }

            return self.create_plan_from_json(fake_json)

        # Real LLM path
        prompt = self._build_prompt(user_input)

        raw_output = self.provider.generate(prompt)

        json_data = self._extract_json(raw_output)

        try:
            return self.create_plan_from_json(json_data)
        except (ValueError, ValidationError):
            repair_prompt = (
                prompt
                + "\n\nYour previous response was invalid."
                + "\nReturn ONLY valid JSON that matches the required schema."
            )

            raw_output = self.provider.generate(repair_prompt)
            json_data = self._extract_json(raw_output)

            return self.create_plan_from_json(json_data)

    # =====================================================
    # PUBLIC JSON ENTRY
    # =====================================================

    def create_plan_from_json(self, json_data: dict) -> ChangePlan:

        try:
            validate(instance=json_data, schema=CHANGE_PLAN_SCHEMA)
        except ValidationError as e:
            raise ValueError(f"Invalid AI JSON format: {e.message}")

        plan = ChangePlan()

        for change in json_data["changes"]:
            change_type = change["type"]
            name = change["name"]

            if change_type == "add_block":
                plan.add_change(AddBlockChange(name))

            elif change_type == "add_item":
                plan.add_change(AddItemChange(name))

            else:
                raise ValueError(f"Unsupported change type: {change_type}")

        return plan

    # =====================================================
    # INTERNAL
    # =====================================================

    def _build_prompt(self, user_input: str) -> str:
        return f"""
You are an AI that converts user requests into JSON change plans.

Return ONLY valid JSON.

User request:
{user_input}

Required JSON format:
{{
  "changes": [
    {{
      "type": "add_block",
      "name": "example_block"
    }}
  ]
}}
"""

    def _extract_json(self, raw_output: str) -> dict:
        try:
            return json.loads(raw_output)
        except json.JSONDecodeError:
            raise ValueError("LLM did not return valid JSON.")

    def _extract_block_name(self, text: str) -> str:
        """
        More flexible extractor:
        supports add/create/make/generate
        """

        text = text.lower()

        match = re.search(
            r"(add|create|make|generate)\s+(\w+)\s+block",
            text
        )

        if match:
            return f"{match.group(2)}_block"

        return "custom_block"