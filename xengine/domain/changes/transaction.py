from xengine.domain.changes.change_plan import ChangePlan
from xengine.validation.change_validator import ChangeValidator
from xengine.platforms.forge.adapter import ForgeAdapter


class Transaction:

    def __init__(self, project_model, platform_adapter=None):
        self.project_model = project_model
        self.platform_adapter = platform_adapter or ForgeAdapter()
        self.validator = ChangeValidator()

    def execute(self, plan: ChangePlan, dry_run: bool = False):

        # 1️⃣ Validate
        self.validator.validate(self.project_model, plan)

        # 2️⃣ Apply
        if not dry_run:
            for change in plan.get_changes():
                change.apply(self.project_model, self.platform_adapter)

        return plan.get_changes()