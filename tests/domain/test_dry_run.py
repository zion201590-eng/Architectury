from xengine.domain.project_model import ProjectModel
from xengine.domain.changes.change_types import AddBlockChange
from xengine.domain.changes.change_plan import ChangePlan
from xengine.domain.changes.transaction import Transaction


def test_dry_run_does_not_modify_project():
    project = ProjectModel("TestMod")

    plan = ChangePlan()
    plan.add_change(AddBlockChange("ruby_block"))

    transaction = Transaction(project)

    # Dry run
    transaction.execute(plan, dry_run=True)

    assert not project.has_entry("ruby_block")