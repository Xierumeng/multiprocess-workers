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
    def create(
        cls, name: str, max_size: int
    ) -> "tuple[True, QueuePropertyData] | tuple[False, None]":
        """
        name: Name of the queue. Must not be empty string.
        max_size: Maximum number of items that can be held in the queue.

        Return: Success, object.
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
    ) -> "tuple[True, WorkerManager] | tuple[False, None]":
        """
        Return: Success, object.
        """
        mp_manager = mp.Manager()

        return True, WorkerManager(cls.__create_key, mp_manager)

    def __init__(
        self, class_private_create_key: object, mp_manager: multiprocessing.managers.SyncManager
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is WorkerManager.__create_key, "Use create() method"

        self.__mp_manager = mp_manager
        self.__names_to_queue: dict[str, queue_wrapper.QueueWrapper] = {}

    def add_queues(self, queue_properties: list[QueuePropertyData]) -> int:
        """
        queue_properties: Property data of the queues to be added.
            Queues must have unique names. A queue with a name that has already been added is rejected. If there are duplicate names in the argument, the queue with the lower index is added and subsequent duplicates are rejected.

        Return: The number of queues added successfully.
        """
        if len(queue_properties) == 0:
            print("ERROR: No queues to create")
            return 0

        count_added = 0
        for queue_property in queue_properties:
            queue_name = queue_property.name
            if queue_name in self.__names_to_queue:
                print(f"ERROR: Skipping queue with duplicate name: {queue_name}")
                continue

            result, queue = queue_wrapper.QueueWrapper.create(
                self.__mp_manager, queue_property.max_size
            )
            if not result:
                print(f"ERROR: Failed to create queue: {queue_name}")
                continue

            # Get Pylance to stop complaining
            assert queue is not None

            self.__names_to_queue[queue_name] = queue
            count_added += 1

        return count_added

    def add_worker():
        pass
