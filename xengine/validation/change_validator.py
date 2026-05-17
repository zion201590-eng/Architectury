from xengine.domain.changes.change_plan import ChangePlan
from xengine.domain.changes.change_types import AddBlockChange, AddItemChange


class ChangeValidationError(Exception):
    pass


class ChangeValidator:

    def validate(self, project_model, plan: ChangePlan):
        for change in plan.get_changes():

            if isinstance(change, AddBlockChange):
                if project_model.has_entry(change.name):
                    raise ChangeValidationError(
                        f"Block '{change.name}' already exists."
                    )

            if isinstance(change, AddItemChange):
                if project_model.has_entry(change.name):
                    raise ChangeValidationError(
                        f"Item '{change.name}' already exists."
                    )