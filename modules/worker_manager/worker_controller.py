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

    __MANAGER_QUEUE_MAX_SIZE = 5

    @classmethod
    def create(cls, mp_manager: multiprocessing.managers.SyncManager) -> tuple[True, "WorkerController"] | tuple[False, None]:
        """
        Return: Success, object.
        """
        return True, WorkerController(cls, mp_manager)

    def __init__(self, class_private_create_key: object, mp_manager: multiprocessing.managers.SyncManager) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is WorkerController.__create_key, "Use create() method"

        self.__pause = mp.BoundedSemaphore(1)

        self.__manager_to_worker_queue = mp_manager.Queue(self.__MANAGER_QUEUE_MAX_SIZE)
        self.__worker_to_manager_queue = mp_manager.Queue(self.__MANAGER_QUEUE_MAX_SIZE)
