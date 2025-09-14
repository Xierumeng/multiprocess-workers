"""
For worker control.
"""

import multiprocessing as mp
import multiprocessing.managers


class WorkerController:
    """
    The worker uses this to communicate with the worker manager.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, mp_manager: multiprocessing.managers.SyncManager, max_size: int
    ) -> tuple[True, "WorkerController"] | tuple[False, None]:
        """
        max_size: Maximum number of items that can be held in the queue. Must be greater than 0.

        Return: Success, object.
        """
        if max_size <= 0:
            print("ERROR: Queue max size must be greater than 0")
            return False, None

        return True, WorkerController(cls.__create_key, mp_manager, max_size)

    def __init__(
        self,
        class_private_create_key: object,
        mp_manager: multiprocessing.managers.SyncManager,
        max_size: int,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is WorkerController.__create_key, "Use create() method"

        self.__pause = mp.BoundedSemaphore(1)

        self.__manager_to_worker_queue = mp_manager.Queue(max_size)
        self.__worker_to_manager_queue = mp_manager.Queue(max_size)
