CHANGE_PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "changes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "name": {"type": "string"}
                },
                "required": ["type", "name"]
            }
        }
    },
    "required": ["changes"]
}