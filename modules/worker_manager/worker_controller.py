"""
For worker control.
"""

import enum
import multiprocessing as mp
import multiprocessing.managers
import queue
import time


class WorkerController:
    """
    The worker uses this to communicate with the worker manager.
    """

    class Command(enum.Enum):
        """
        Worker commands.
        """
        Exit = 1

    class Heartbeat:
        """
        Heartbeat to inform worker manager that the worker is alive.
        """
        def __init__(self) -> None:
            """
            Adds local timestamp.
            """
            self.timestamp = time.time()

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

        self.__manager_to_worker_exit_queue = mp_manager.Queue(1)

        self.__worker_to_manager_queue = mp_manager.Queue(max_size)

    def worker_heartbeat(self) -> None:
        """
        To be called by worker.

        Informs the manager that the worker is still alive.

        Return: None.
        """
        heartbeat = WorkerController.Heartbeat()

        # TODO: Rate limit
        try:
            self.__worker_to_manager_queue.put_nowait(heartbeat)
        except queue.Full as exception:
            print(f"WARN: Worker to manager queue is being overrun: {exception}")

    def worker_check_pause(self) -> None:
        """
        To be called by worker.

        Check if pause has been requested.

        Return: None.
        """
        self.__pause.acquire()
        self.__pause.release()

    def worker_check_exit(self) -> bool:
        """
        To be called by worker.

        Check if exit has been requested.

        Return: Is exit commanded.
        """
        return not self.__manager_to_worker_exit_queue.empty()

    def manager_command_pause(self, timeout: float) -> bool:
        """
        To be called by manager.

        Commands worker to pause.

        Return: Success.
        """
        return self.__pause.acquire(timeout=timeout)

    def manager_command_resume(self) -> bool:
        """
        To be called by manager.

        Commands worker to resume.

        Return: Success.
        """
        try:
            self.__pause.release()
        except ValueError as exception:
            print(f"WARN: Worker controller pause semaphore already released: {exception}")

        return True

    def manager_command_exit(self) -> bool:
        """
        To be called by manager.

        Commands worker to exit.

        Return: Success.
        """
        try:
            self.__manager_to_worker_exit_queue.put_nowait(WorkerController.Command.Exit)
        except queue.Full as exception:
            print(f"WARN: Manager to worker exit queue already has exit command: {exception}")

        return True
