from typing import List
from xengine.domain.changes.change_types import Change


class ChangePlan:

    def __init__(self):
        self._changes: List[Change] = []

    def add_change(self, change: Change):
        self._changes.append(change)

    def get_changes(self) -> List[Change]:
        return list(self._changes)

    def explain(self) -> list[str]:
        return [change.explain() for change in self._changes]

    def to_dict(self) -> list[dict]:
        return [change.to_dict() for change in self._changes]