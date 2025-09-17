"""
Test worker.
"""

import multiprocessing as mp

import pytest

from modules.worker_manager import queue_property_data
from modules.worker_manager import queue_wrapper
from modules.worker_manager import worker_controller
from modules.worker_manager.private import process_property_data


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

    def test_normal_1(self) -> None:
        """
        Normal.
        """
        result, worker = process_property_data.ProcessPropertyData.create(stub1, (), [], [])

        assert result
        assert worker is not None

    def test_normal_2(
        self,
        input_queues: list[queue_wrapper.QueueWrapper],
        output_queues: list[queue_wrapper.QueueWrapper],
    ) -> None:
        """
        Normal.
        """
        result, worker = process_property_data.ProcessPropertyData.create(
            stub2,
            (0, ""),
            input_queues,
            output_queues,
        )

        assert result
        assert worker is not None

    def test_input_queues_empty(
        self,
        output_queues: list[queue_wrapper.QueueWrapper],
    ) -> None:
        """
        Input queues empty.
        """
        result, worker = process_property_data.ProcessPropertyData.create(
            stub2,
            (0, ""),
            [],
            output_queues,
        )

        assert not result
        assert worker is None

    def test_output_queues_empty(
        self,
        input_queues: list[queue_wrapper.QueueWrapper],
    ) -> None:
        """
        Output queues empty.
        """
        result, worker = process_property_data.ProcessPropertyData.create(
            stub2,
            (0, ""),
            input_queues,
            [],
        )

        assert not result
        assert worker is None

    def test_input_queues_extra(
        self,
        input_queues: list[queue_wrapper.QueueWrapper],
        output_queues: list[queue_wrapper.QueueWrapper],
    ) -> None:
        """
        Input queues too many.
        """
        result, worker = process_property_data.ProcessPropertyData.create(
            stub2,
            (0, ""),
            input_queues + output_queues,
            output_queues,
        )

        assert not result
        assert worker is None

    def test_output_queues_extra(
        self,
        input_queues: list[queue_wrapper.QueueWrapper],
        output_queues: list[queue_wrapper.QueueWrapper],
    ) -> None:
        """
        Output queues too many.
        """
        result, worker = process_property_data.ProcessPropertyData.create(
            stub2,
            (0, ""),
            input_queues,
            output_queues + input_queues,
        )

        assert not result
        assert worker is None

    def test_queues_wrong_name(
        self,
        input_queues: list[queue_wrapper.QueueWrapper],
        output_queues: list[queue_wrapper.QueueWrapper],
    ) -> None:
        """
        Mixed up queues.
        """
        result, worker = process_property_data.ProcessPropertyData.create(
            stub2,
            (0, ""),
            output_queues,
            input_queues,
        )

        assert not result
        assert worker is None
