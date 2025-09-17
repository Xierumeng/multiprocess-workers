"""
Worker group.
"""

import multiprocessing.managers

from . import process_property_data
from . import process_wrapper
from .. import worker_controller


class WorkerGroup:
    """
    Processes with the same target function.
    """

    __create_key = object()

    @classmethod
    def create(
        cls,
        count: int,
        process_property: process_property_data.ProcessPropertyData,
        mp_manager: multiprocessing.managers.SyncManager,
        controller_max_size: int,
    ) -> tuple[True, "WorkerGroup"] | tuple[False, None]:
        """
        count: Number of workers.
        process_property: Property data of the worker.
        mp_manager: For the worker controller.
        controller_max_size: For the worker controller.

        Return: Success, object.
        """
        if count <= 0:
            print(f"ERROR: No workers for {process_property.get_target_function()}")
            return False, None

        # It is okay to drop these process handles since the workers have not been started.
        workers: list[process_wrapper.ProcessWrapper] = []
        for _ in range(0, count):
            result, controller = worker_controller.WorkerController.create(
                mp_manager, controller_max_size
            )
            if not result:
                print(
                    f"ERROR: Failed to create worker controller for: {process_property.get_target_function()}"
                )
                return False, None

            # Get Pylance to stop complaining
            assert controller is not None

            result, worker = process_wrapper.ProcessWrapper.create(process_property, controller)
            if not result:
                print(
                    f"ERROR: Failed to create process for: {process_property.get_target_function()}"
                )
                return False, None

            # Get Pylance to stop complaining
            assert worker is not None

            workers.append(worker)

        return True, WorkerGroup(
            cls.__create_key, workers, count, process_property, mp_manager, controller_max_size
        )

    def __init__(
        self,
        class_private_create_key: object,
        workers: list[process_wrapper.ProcessWrapper],
        count: int,
        process_property: process_property_data.ProcessPropertyData,
        mp_manager: multiprocessing.managers.SyncManager,
        controller_max_size: int,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is WorkerGroup.__create_key, "Use create() method"

        # TODO: Start using these
        # pylint: disable=unused-private-member
        self.__workers = workers

        self.__count = count
        self.__process_property = process_property
        self.__mp_manager = mp_manager
        self.__controller_max_size = controller_max_size
        # pylint: enable=unused-private-member
