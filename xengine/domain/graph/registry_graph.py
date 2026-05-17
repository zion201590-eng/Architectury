from dataclasses import dataclass
from typing import Dict, List


@dataclass
class RegistryEntry:
    name: str
    entry_type: str  # block, item, etc.


class RegistryGraph:
    def __init__(self):
        self._entries: Dict[str, RegistryEntry] = {}

    def add_entry(self, name: str, entry_type: str) -> None:
        if name in self._entries:
            raise ValueError(f"Registry entry '{name}' already exists.")

        self._entries[name] = RegistryEntry(
            name=name,
            entry_type=entry_type,
        )

    def has_entry(self, name: str) -> bool:
        return name in self._entries

    def get_entry(self, name: str) -> RegistryEntry:
        if name not in self._entries:
            raise ValueError(f"Registry entry '{name}' does not exist.")

        return self._entries[name]

    def list_entries(self) -> List[RegistryEntry]:
        return list(self._entries.values())