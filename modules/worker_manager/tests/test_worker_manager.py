"""
Test worker manager.
"""

import pytest

from modules.worker_manager import worker_manager


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


@pytest.fixture
def queue_properties() -> list[worker_manager.QueuePropertyData]:  # type: ignore
    """
    Some queue properties in a list.
    """
    max_size = 5

    result, queue_property_1 = worker_manager.QueuePropertyData.create("1", max_size)
    assert result
    assert queue_property_1 is not None

    result, queue_property_2 = worker_manager.QueuePropertyData.create("2", max_size)
    assert result
    assert queue_property_2 is not None

    yield [queue_property_1, queue_property_2]  # type: ignore


class TestCreate:
    """
    Test create() method.
    """
    def test_normal(self, queue_properties: list[worker_manager.QueuePropertyData]) -> None:
        """
        Normal.
        """
        result, manager = worker_manager.WorkerManager.create(queue_properties)

        assert result
        assert manager is not None


    def test_queue_properties_empty(self) -> None:
        """
        Empty queue_properties.
        """
        result, manager = worker_manager.WorkerManager.create([])

        assert not result
        assert manager is None

    def test_queue_properties_with_duplicate(self, queue_properties: list[worker_manager.QueuePropertyData]) -> None:
        """
        Duplicate entry in queue_properties.
        """
        queue_properties.append(queue_properties[0])

        result, manager = worker_manager.WorkerManager.create(queue_properties)

        assert not result
        assert manager is None
