"""
Test worker manager.
"""

import pytest

from modules.worker_manager import queue_property_data
from modules.worker_manager import queue_wrapper
from modules.worker_manager import worker_controller
from modules.worker_manager import worker_manager
from modules.worker_manager import worker_property_data


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


@pytest.fixture
def manager_empty() -> worker_manager.WorkerManager:  # type: ignore
    """
    Worker manager.
    """
    result, manager = worker_manager.WorkerManager.create(5)
    assert result
    assert manager is not None

    yield manager  # type: ignore


@pytest.fixture
def queue_properties() -> list[queue_property_data.QueuePropertyData]:  # type: ignore
    """
    Some queue property data in a list.
    """
    max_size = 5

    result, queue_property_1 = queue_property_data.QueuePropertyData.create("1", max_size)
    assert result
    assert queue_property_1 is not None

    result, queue_property_2 = queue_property_data.QueuePropertyData.create("2", max_size)
    assert result
    assert queue_property_2 is not None

    yield [queue_property_1, queue_property_2]  # type: ignore


@pytest.fixture
def more_queue_properties() -> list[queue_property_data.QueuePropertyData]:  # type: ignore
    """
    More queue property data in a lsit.
    """
    max_size = 5

    result, queue_property_3 = queue_property_data.QueuePropertyData.create("3", max_size)
    assert result
    assert queue_property_3 is not None

    result, queue_property_4 = queue_property_data.QueuePropertyData.create("4", max_size)
    assert result
    assert queue_property_4 is not None

    yield [queue_property_3, queue_property_4]  # type: ignore


@pytest.fixture
def manager_with_queues(
    manager_empty: worker_manager.WorkerManager,
    queue_properties: list[queue_property_data.QueuePropertyData],
    more_queue_properties: list[queue_property_data.QueuePropertyData],
) -> worker_manager.WorkerManager:  # type: ignore
    """
    Worker manager with queues.
    """
    count_added = manager_empty.add_queues(queue_properties)
    assert count_added == len(queue_properties)

    count_added = manager_empty.add_queues(more_queue_properties)
    assert count_added == len(more_queue_properties)

    yield manager_empty  # type: ignore


@pytest.fixture
def manager_with_input_queues_only(
    manager_empty: worker_manager.WorkerManager,
    queue_properties: list[queue_property_data.QueuePropertyData],
) -> worker_manager.WorkerManager:  # type: ignore
    """
    Worker manager with queues.
    """
    count_added = manager_empty.add_queues(queue_properties)
    assert count_added == len(queue_properties)

    yield manager_empty  # type: ignore


@pytest.fixture
def manager_with_output_queues_only(
    manager_empty: worker_manager.WorkerManager,
    more_queue_properties: list[queue_property_data.QueuePropertyData],
) -> worker_manager.WorkerManager:  # type: ignore
    """
    Worker manager with queues.
    """
    count_added = manager_empty.add_queues(more_queue_properties)
    assert count_added == len(more_queue_properties)

    yield manager_empty  # type: ignore


@pytest.fixture
def worker_properties() -> list[worker_property_data.WorkerPropertyData]:  # type: ignore
    """
    Some worker property data in a list.
    """
    count = 1

    # Stub function.
    # pylint: disable=unused-argument
    def stub1(controller: worker_controller.WorkerController) -> None:
        """
        Stub function.
        """

    # pylint: enable=unused-argument

    # Stub function.
    # pylint: disable=unused-argument
    def stub2(
        i: int,
        s: str,
        input_queue_1: queue_wrapper.QueueWrapper,
        input_queue_2: queue_wrapper.QueueWrapper,
        output_queue_1: queue_wrapper.QueueWrapper,
        output_queue_2: queue_wrapper.QueueWrapper,
        controller: worker_controller.WorkerController,
    ) -> None:
        """
        Stub function.
        """

    # pylint: enable=unused-argument

    args2 = (2, "test")
    input_queue_names_2 = ["1", "2"]
    output_queue_names_2 = ["3", "4"]

    result, worker_property_1 = worker_property_data.WorkerPropertyData.create(
        count, stub1, (), [], []
    )
    assert result
    assert worker_property_1 is not None

    result, worker_property_2 = worker_property_data.WorkerPropertyData.create(
        count, stub2, args2, input_queue_names_2, output_queue_names_2
    )
    assert result
    assert worker_property_2 is not None

    yield [worker_property_1, worker_property_2]  # type: ignore


class TestAddQueues:
    """
    Test add_queues() method.
    """

    def test_normal(
        self,
        manager_empty: worker_manager.WorkerManager,
        queue_properties: list[queue_property_data.QueuePropertyData],
    ) -> None:
        """
        Normal.
        """
        count_added = manager_empty.add_queues(queue_properties)

        assert count_added == len(queue_properties)

    def test_empty(self, manager_empty: worker_manager.WorkerManager) -> None:
        """
        Empty queue_properties.
        """
        count_added = manager_empty.add_queues([])

        assert count_added == 0

    def test_duplicate_in_argument(
        self,
        manager_empty: worker_manager.WorkerManager,
        queue_properties: list[queue_property_data.QueuePropertyData],
    ) -> None:
        """
        Duplicate name in queue_properties.
        """
        queue_properties.append(queue_properties[0])

        count_added = manager_empty.add_queues(queue_properties)

        assert count_added == 2

    def test_duplicate_in_manager(
        self,
        manager_empty: worker_manager.WorkerManager,
        queue_properties: list[queue_property_data.QueuePropertyData],
    ) -> None:
        """
        Duplicate name already in manager.
        """
        count_added = manager_empty.add_queues(queue_properties[0:1])
        assert count_added == 1

        count_added = manager_empty.add_queues(queue_properties)
        assert count_added == 1

        count_added = manager_empty.add_queues(queue_properties)
        assert count_added == 0


class TestAddWorkerGroups:
    """
    Test add_worker_groups method.
    """

    def test_normal(
        self,
        manager_with_queues: worker_manager.WorkerManager,
        worker_properties: list[worker_property_data.WorkerPropertyData],
    ) -> None:
        """
        Normal.
        """
        count_added = manager_with_queues.add_worker_groups(worker_properties)

        assert count_added == len(worker_properties)

    def test_empty(
        self,
        manager_with_queues: worker_manager.WorkerManager,
    ) -> None:
        """
        Empty worker_properties.
        """
        count_added = manager_with_queues.add_worker_groups([])

        assert count_added == 0

    def test_duplicate_function_name_in_argument(
        self,
        manager_with_queues: worker_manager.WorkerManager,
        worker_properties: list[worker_property_data.WorkerPropertyData],
    ) -> None:
        """
        Duplicate name in worker_properties.
        """
        worker_properties.append(worker_properties[0])

        count_added = manager_with_queues.add_worker_groups(worker_properties)

        assert count_added == 2

    def test_duplicate_function_name_in_manager(
        self,
        manager_with_queues: worker_manager.WorkerManager,
        worker_properties: list[worker_property_data.WorkerPropertyData],
    ) -> None:
        """
        Duplicate name already in manager.
        """
        count_added = manager_with_queues.add_worker_groups(worker_properties[0:1])
        assert count_added == 1

        count_added = manager_with_queues.add_worker_groups(worker_properties)
        assert count_added == 1

        count_added = manager_with_queues.add_worker_groups(worker_properties)
        assert count_added == 0

    def test_input_queue_name_not_in_manager(
        self,
        manager_with_output_queues_only: worker_manager.WorkerManager,
        worker_properties: list[worker_property_data.WorkerPropertyData],
    ) -> None:
        """
        Input queue does not exist in manager.
        """
        count_added = manager_with_output_queues_only.add_worker_groups(worker_properties)

        assert count_added == 1

    def test_output_queue_name_not_in_manager(
        self,
        manager_with_input_queues_only: worker_manager.WorkerManager,
        worker_properties: list[worker_property_data.WorkerPropertyData],
    ) -> None:
        """
        Output queue does not exist in manager.
        """
        count_added = manager_with_input_queues_only.add_worker_groups(worker_properties)

        assert count_added == 1
