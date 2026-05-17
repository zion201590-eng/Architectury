from xengine.domain.project_model import ProjectModel
from xengine.domain.changes.change_types import AddBlockChange
from xengine.domain.changes.change_plan import ChangePlan
from xengine.domain.changes.transaction import Transaction


def test_add_block_via_change_plan():
    project = ProjectModel("TestMod")

    plan = ChangePlan()
    plan.add_change(AddBlockChange("ruby_block"))

    transaction = Transaction(project)
    transaction.execute(plan)

    assert project.has_entry("ruby_block")