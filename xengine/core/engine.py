from typing import Optional, List

from xengine.domain.project_model import ProjectModel
from xengine.domain.changes.change_plan import ChangePlan
from xengine.domain.changes.change_types import AddBlockChange
from xengine.domain.changes.transaction import Transaction
from xengine.platforms.base.adapter import PlatformAdapter
from xengine.platforms.forge.adapter import ForgeAdapter
from xengine.core.ai_planner import AIPlanner
from xengine.core.llm.mock_provider import MockProvider
from xengine.execution.file_system_gateway import FileSystemGateway


class Engine:

    def __init__(
        self,
        project_model: ProjectModel,
        platform_adapter: Optional[PlatformAdapter] = None,
        llm_provider=None,
        project_root: Optional[str] = None,
    ):
        self.project_model = project_model
        self.platform_adapter = platform_adapter or ForgeAdapter()

        self.transaction = Transaction(
            project_model=self.project_model,
            platform_adapter=self.platform_adapter,
        )

        self.ai_planner = AIPlanner(
            provider=llm_provider or MockProvider()
        )

        # ✅ File system layer
        self.fs_gateway = (
            FileSystemGateway(project_root) if project_root else None
        )

        self._pending_plan: Optional[ChangePlan] = None
        self._history: List[ChangePlan] = []

    # -------------------------------------------------

    def preview(self, user_input: str):
        plan = self.ai_planner.plan_from_user_input(user_input)

        self.transaction.execute(plan, dry_run=True)

        self._pending_plan = plan

        return plan.get_changes()

    def confirm(self):
        if not self._pending_plan:
            raise ValueError("No pending changes to confirm.")

        # Apply to domain
        self.transaction.execute(self._pending_plan, dry_run=False)

        # ✅ Generate files if fs enabled
        if self.fs_gateway:
            self._generate_files(self._pending_plan)

        self._history.append(self._pending_plan)

        applied_changes = self._pending_plan.get_changes()

        self._pending_plan = None

        return applied_changes

    def undo(self):
        if not self._history:
            raise ValueError("No changes to undo.")

        last_plan = self._history.pop()

        for change in reversed(last_plan.get_changes()):
            change.rollback(self.project_model)

    # -------------------------------------------------

    def _generate_files(self, plan: ChangePlan):

        for change in plan.get_changes():

            if isinstance(change, AddBlockChange):
                if hasattr(self.platform_adapter, "generate_block_files"):
                    self.platform_adapter.generate_block_files(
                        self.fs_gateway,
                        change.name
                    )