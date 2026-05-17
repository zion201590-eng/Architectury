import pytest
from xengine.domain.project_model import ProjectModel
from xengine.domain.changes.change_types import AddBlockChange
from xengine.domain.changes.change_plan import ChangePlan
from xengine.domain.changes.transaction import Transaction
from xengine.validation.change_validator import ChangeValidationError


def test_duplicate_block_fails_validation():
    project = ProjectModel("TestMod")

    plan1 = ChangePlan()
    plan1.add_change(AddBlockChange("ruby_block"))

    Transaction(project).execute(plan1)

    plan2 = ChangePlan()
    plan2.add_change(AddBlockChange("ruby_block"))

    with pytest.raises(ChangeValidationError):
        Transaction(project).execute(plan2)