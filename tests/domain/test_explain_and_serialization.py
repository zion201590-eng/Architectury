from xengine.domain.changes.change_types import AddBlockChange
from xengine.domain.changes.change_plan import ChangePlan


def test_change_explain():
    change = AddBlockChange("ruby_block")
    assert "ruby_block" in change.explain()


def test_change_plan_serialization():
    plan = ChangePlan()
    plan.add_change(AddBlockChange("ruby_block"))

    data = plan.to_dict()

    assert isinstance(data, list)
    assert data[0]["type"] == "AddBlockChange"
    assert data[0]["name"] == "ruby_block"