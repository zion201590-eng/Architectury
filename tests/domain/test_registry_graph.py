import pytest
from xengine.domain.graph.registry_graph import RegistryGraph


def test_add_entry():
    registry = RegistryGraph()
    registry.add_entry("ruby_block", "block")

    assert registry.has_entry("ruby_block")


def test_duplicate_entry_raises():
    registry = RegistryGraph()
    registry.add_entry("ruby_block", "block")

    with pytest.raises(ValueError):
        registry.add_entry("ruby_block", "block")