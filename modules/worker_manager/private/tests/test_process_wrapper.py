"""
Test worker.
"""

import multiprocessing as mp

import pytest

from modules.worker_manager import queue_property_data
from modules.worker_manager import queue_wrapper
from modules.worker_manager import worker_controller
from modules.worker_manager.private import process_wrapper


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


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


@pytest.fixture
def controller() -> worker_controller.WorkerController:  # type: ignore
    """
    Worker controller.
    """
    mp_manager = mp.Manager()
    result, controller = worker_controller.WorkerController.create(mp_manager, 5)
    assert result
    assert controller is not None

    yield controller  # type: ignore


@pytest.fixture
def input_queues() -> list[queue_wrapper.QueueWrapper]:  # type: ignore
    """
    Input queues.
    """
    mp_manager = mp.Manager()

    result, queue_properties_1 = queue_property_data.QueuePropertyData.create("input_queue_1", 5)
    assert result
    assert queue_properties_1 is not None

    result, queue_1 = queue_wrapper.QueueWrapper.create(mp_manager, queue_properties_1)
    assert result
    assert queue_1 is not None

    result, queue_properties_2 = queue_property_data.QueuePropertyData.create("input_queue_2", 5)
    assert result
    assert queue_properties_2 is not None

    result, queue_2 = queue_wrapper.QueueWrapper.create(mp_manager, queue_properties_2)
    assert result
    assert queue_2 is not None

    yield [queue_1, queue_2]  # type: ignore


@pytest.fixture
def output_queues() -> list[queue_wrapper.QueueWrapper]:  # type: ignore
    """
    Output queues.
    """
    mp_manager = mp.Manager()

    result, queue_properties_1 = queue_property_data.QueuePropertyData.create("output_queue_1", 5)
    assert result
    assert queue_properties_1 is not None

    result, queue_1 = queue_wrapper.QueueWrapper.create(mp_manager, queue_properties_1)
    assert result
    assert queue_1 is not None

    result, queue_properties_2 = queue_property_data.QueuePropertyData.create("output_queue_2", 5)
    assert result
    assert queue_properties_2 is not None

    result, queue_2 = queue_wrapper.QueueWrapper.create(mp_manager, queue_properties_2)
    assert result
    assert queue_2 is not None

    yield [queue_1, queue_2]  # type: ignore


class TestCreate:
    """
    Test create() method.
    """

    def test_normal_1(self, controller: worker_controller.WorkerController) -> None:
        """
        Normal.
        """
        result, worker = process_wrapper.ProcessWrapper.create(stub1, (), [], [], controller)

        assert result
        assert worker is not None

    def test_normal_2(
        self,
        input_queues: list[queue_wrapper.QueueWrapper],
        output_queues: list[queue_wrapper.QueueWrapper],
        controller: worker_controller.WorkerController,
    ) -> None:
        """
        Normal.
        """
        result, worker = process_wrapper.ProcessWrapper.create(
            stub2, (0, ""), input_queues, output_queues, controller
        )

        assert result
        assert worker is not None
