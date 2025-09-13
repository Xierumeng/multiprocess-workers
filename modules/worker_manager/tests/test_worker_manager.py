"""
Test worker manager.
"""

import pytest

from modules.worker_manager import worker_manager


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


@pytest.fixture
def manager() -> worker_manager.WorkerManager:  # type: ignore
    """
    Worker manager.
    """
    result, manager = worker_manager.WorkerManager.create()
    assert result
    assert manager is not None

    yield manager  # type: ignore


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


class TestAddQueues:
    """
    Test add_queues() method.
    """

    def test_normal(
        self,
        manager: worker_manager.WorkerManager,
        queue_properties: list[worker_manager.QueuePropertyData],
    ) -> None:
        """
        Normal.
        """
        count_added = manager.add_queues(queue_properties)

        assert count_added == len(queue_properties)

    def test_empty(self, manager: worker_manager.WorkerManager) -> None:
        """
        Empty queue_properties.
        """
        count_added = manager.add_queues([])

        assert count_added == 0

    def test_duplicate_in_argument(
        self,
        manager: worker_manager.WorkerManager,
        queue_properties: list[worker_manager.QueuePropertyData],
    ) -> None:
        """
        Duplicate entry in queue_properties.
        """
        queue_properties.append(queue_properties[0])

        count_added = manager.add_queues(queue_properties)

        assert count_added == 2

    def test_duplicate_in_manager(
        self,
        manager: worker_manager.WorkerManager,
        queue_properties: list[worker_manager.QueuePropertyData],
    ) -> None:
        """
        Duplicate entry already in manager.
        """
        count_added = manager.add_queues(queue_properties[0:1])
        assert count_added == 1

        count_added = manager.add_queues(queue_properties)
        assert count_added == 1

        count_added = manager.add_queues(queue_properties)
        assert count_added == 0
