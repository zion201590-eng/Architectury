import pytest
from xengine.core.ai_planner import AIPlanner


def test_invalid_json_fails_schema():
    planner = AIPlanner()

    invalid_json = {
        "changes": [
            {
                "type": "add_block"
                # missing "name"
            }
        ]
    }

    with pytest.raises(ValueError):
        planner.create_plan_from_json(invalid_json)