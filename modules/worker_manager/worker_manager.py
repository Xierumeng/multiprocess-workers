"""
Worker manager.
"""

import multiprocessing as mp
import multiprocessing.managers

from . import queue_property_data
from . import queue_wrapper
from . import worker_property_data
from .private import process_property_data
from .private import worker_group


class WorkerManager:
    """
    Starts and monitors workers.
    """

    __create_key = object()

    @classmethod
    def create(
        cls,
        controller_max_size: int,
    ) -> tuple[True, "WorkerManager"] | tuple[False, None]:
        """
        controller_max_size: Maximum number of items that can be held in each of the worker controllers' queues. Must be greater than 0.

        Return: Success, object.
        """
        if controller_max_size <= 0:
            print("ERROR: Queue max size must be greater than 0")
            return False, None

        mp_manager = mp.Manager()

        return True, WorkerManager(cls.__create_key, mp_manager, controller_max_size)

    def __init__(
        self,
        class_private_create_key: object,
        mp_manager: multiprocessing.managers.SyncManager,
        controller_max_size: int,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is WorkerManager.__create_key, "Use create() method"

        self.__mp_manager = mp_manager

        self.__names_to_queue: dict[str, queue_wrapper.QueueWrapper] = {}

        self.__controller_max_size = controller_max_size
        self.__names_to_worker_group: dict[str, worker_group.WorkerGroup] = {}

    def add_queues(self, queue_properties: list[queue_property_data.QueuePropertyData]) -> int:
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
                self.__mp_manager,
                queue_property,
            )
            if not result:
                print(f"ERROR: Failed to create queue: {queue_name}")
                continue

            # Get Pylance to stop complaining
            assert queue is not None

            self.__names_to_queue[queue_name] = queue
            count_added += 1

        return count_added

    def add_worker_groups(
        self, worker_properties: list[worker_property_data.WorkerPropertyData]
    ) -> int:
        """
        worker_properties: Property data of the worker groups to be added.

        Return: The number of worker groups added successfully.
        """
        if len(worker_properties) == 0:
            print("ERROR: No worker groups to add")
            return 0

        count_added = 0
        for worker_property in worker_properties:
            result = self.__add_worker_group(worker_property)
            if not result:
                continue

            count_added += 1

        return count_added

    def __add_worker_group(self, worker_property: worker_property_data.WorkerPropertyData) -> bool:
        """
        worker_property: Property data of the worker to be added.

        Return: Success.
        """
        worker_name = worker_property.target_function.__name__
        if worker_name in self.__names_to_worker_group:
            print(f"ERROR: Skipping worker group with duplicate name: {worker_name}")
            return False

        result, input_queues = self.__get_queues(
            self.__names_to_queue, worker_property.input_queue_names
        )
        if not result:
            print(
                f"ERROR: The worker group's input queue name does not exist, failed to create worker group: {worker_name}"
            )
            return False

        # Get Pylance to stop complaining
        assert input_queues is not None

        result, output_queues = self.__get_queues(
            self.__names_to_queue, worker_property.output_queue_names
        )
        if not result:
            print(
                f"ERROR: The worker group's output queue name does not exist, failed to create worker group: {worker_name}"
            )
            return False

        # Get Pylance to stop complaining
        assert output_queues is not None

        result, process_property = process_property_data.ProcessPropertyData.create(
            worker_property.target_function,
            worker_property.target_arguments,
            input_queues,
            output_queues,
        )
        if not result:
            print(f"ERROR: Failed to create worker properties: {worker_name}")
            return False

        # Get Pylance to stop complaining
        assert process_property is not None

        result, group = worker_group.WorkerGroup.create(
            worker_property.count, process_property, self.__mp_manager, self.__controller_max_size
        )
        if not result:
            print(f"ERROR: Failed to create workers: {worker_name}")
            return False

        # Get Pylance to stop complaining
        assert group is not None

        self.__names_to_worker_group[worker_name] = group

        return True

    @staticmethod
    def __get_queues(
        names_to_queue: dict[str, queue_wrapper.QueueWrapper], names: list[str]
    ) -> tuple[True, list[queue_wrapper.QueueWrapper]] | tuple[False, None]:
        """
        Get queues given the requested names.
        """
        queues: list[queue_wrapper.QueueWrapper] = []
        for name in names:
            if not name in names_to_queue:
                print(f"ERROR: Missing item: {name}")
                return False, None

            queue = names_to_queue[name]
            queues.append(queue)

        return True, queues
