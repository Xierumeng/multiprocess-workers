"""
Worker manager.
"""

import multiprocessing as mp
import multiprocessing.managers

from . import queue_wrapper


class QueuePropertyData:
    """
    Properties about the queue.
    """

    __create_key = object()

    @classmethod
    def create(cls, name: str, max_size: int) -> "tuple[True, QueuePropertyData] | tuple[False, None]":
        """
        name: Name of the queue. Must not be empty string.
        max_size: Maximum number of items that can be held in the queue.
        """
        if name == "":
            print("ERROR: Name cannot be empty")
            return False, None

        if max_size <= 0:
            print("ERROR: Queue max size must be greater than 0")
            return False, None

        return True, QueuePropertyData(cls.__create_key, name, max_size)

    def __init__(self, class_private_create_key: object, name: str, max_size: int) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is QueuePropertyData.__create_key, "Use create() method"

        self.name = name
        self.max_size = max_size


class WorkerPropertyData:
    """
    Properties about the worker.
    """

    __create_key = object()

    @classmethod
    def create(
        cls,
        count: int,
        target_function: "(...) -> object",  # type: ignore
        target_arguments: tuple,
        input_queues: list[queue_wrapper.QueueWrapper],
        output_queues: list[queue_wrapper.QueueWrapper],
    ):
        pass


class WorkerManager:
    """
    Starts and monitors workers.
    """

    __create_key = object()

    @classmethod
    def create(
        cls,
        queue_properties: list[QueuePropertyData],
    ) -> "tuple[True, WorkerManager] | tuple[False, None]":
        """
        queue_properties: Properties for each queue. Names must be unique.
        """
        if len(queue_properties) == 0:
            print("ERROR: No queues to create")
            return False, None

        # Check for duplicate names
        names = set()
        for queue_property in queue_properties:
            name = queue_property.name
            if name in names:
                print(f"ERROR: Duplicate name: {name}")
                return False, None

            names.add(name)

        mp_manager = mp.Manager()

        names_to_queue: dict[str, queue_wrapper.QueueWrapper] = {}
        for queue_property in queue_properties:
            result, queue = queue_wrapper.QueueWrapper.create(mp_manager, queue_property.max_size)
            if not result:
                print("ERROR: Failed to create queue")
                return False, None

            # Get Pylance to stop complaining
            assert queue is not None

            names_to_queue[queue_property.name] = queue

        return True, WorkerManager(cls.__create_key, mp_manager, names_to_queue)

    def __init__(self, class_private_create_key: object, mp_manager: multiprocessing.managers.SyncManager, names_to_queue: dict[str, queue_wrapper.QueueWrapper]) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is WorkerManager.__create_key, "Use create() method"

        self.__mp_manager = mp_manager
        self.__names_to_queue = names_to_queue


    def add_worker():
        pass

    def add_queue():
        pass
