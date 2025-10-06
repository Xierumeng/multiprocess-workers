"""
Process.
"""

import enum
import multiprocessing as mp

from . import process_property_data
from .. import worker_controller


class ProcessWrapper:
    """
    Wrapper for an underlying process and other information.
    """

    class State(enum.Enum):
        """
        State of the process.
        """

        READY = 1
        RUNNING_HEALTHY = 2
        RUNNING_TIMEOUT = 3
        PAUSED = 4
        EXITED = 5

    __create_key = object()

    @classmethod
    def create(
        cls,
        process_property: process_property_data.ProcessPropertyData,
        controller: worker_controller.WorkerController,
    ) -> tuple[True, "ProcessWrapper"] | tuple[False, None]:
        """
        process_property: Process data of the process to be created.
        controller: Worker controller.

        Return: Success, object.
        """

        target_function = process_property.get_target_function()
        arguments = process_property.get_arguments() + (controller,)

        try:
            worker = mp.Process(target=target_function, args=arguments)
        # Catching all exceptions for library call
        # pylint: disable-next=broad-exception-caught
        except Exception as exception:
            print(f"ERROR: Failed to create worker process: {exception}")
            return False, None

        return True, ProcessWrapper(cls.__create_key, worker, controller)

    def __init__(
        self,
        class_private_create_key: object,
        worker: mp.Process,
        controller: worker_controller.WorkerController,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is ProcessWrapper.__create_key, "Use create() method"

        self.__worker = worker
        self.__controller = controller

        self.__state = ProcessWrapper.State.READY

    def __del__(self) -> None:
        """
        Destructor.
        """
        if self.__state == ProcessWrapper.State.EXITED:
            return

        self.stop(0)

    def start(self) -> bool:
        """
        Start the process.

        TODO: Consider RAII, worker starts on construction.

        Return: Success.
        """
        if self.__state != ProcessWrapper.State.READY:
            print(f"ERROR: Process {self.__worker.ident} has already started")
            return False

        self.__worker.start()

        self.__state = ProcessWrapper.State.RUNNING_HEALTHY

        return True

    def pause(self) -> bool:
        """
        Pause the process.

        Return: Success.
        """
        if self.__state != (
            ProcessWrapper.State.RUNNING_HEALTHY or ProcessWrapper.State.RUNNING_TIMEOUT
        ):
            print(f"ERROR: Process {self.__worker.ident} is not running")
            return False

        # TODO: Unhardcode timeout
        result = self.__controller.manager_command_pause(0.1)
        if not result:
            print(f"ERROR: Controller failed to command process {self.__worker.ident} to pause")
            return False

        self.__state = ProcessWrapper.State.PAUSED

        return True

    def resume(self) -> bool:
        """
        Resume the process.

        Return: Success.
        """
        if self.__state != ProcessWrapper.State.PAUSED:
            print(f"ERROR: Process {self.__worker.ident} is not paused")
            return False

        result = self.__controller.manager_command_resume()
        if not result:
            print(f"ERROR: Controller failed to command process {self.__worker.ident} to resume")
            return False

        self.__state = ProcessWrapper.State.RUNNING_HEALTHY

        return True

    def stop(self, timeout: float) -> bool:
        """
        Stop the process. On timeout, terminate the process.

        TODO: Consider RAII, worker stops on destruction.

        Return: Success.
        """
        if self.__state == ProcessWrapper.State.READY:
            print("ERROR: Process has not started")
            return False

        if self.__state == ProcessWrapper.State.EXITED:
            print(f"ERROR: Process {self.__worker.ident} is already stopped")
            return False

        if timeout < 0:
            print("ERROR: Timeout cannot be negative")
            return False

        if self.__state == ProcessWrapper.State.PAUSED:
            self.resume()

        result = self.__controller.manager_command_exit()
        if not result:
            print(
                f"WARN: Controller failed to command process {self.__worker.ident} to exit, terminating"
            )
            self.__worker.terminate()

            return True

        self.__worker.join(timeout)

        exit_code = self.__worker.exitcode
        if exit_code is None:
            print(f"WARN: Process {self.__worker.ident} is still active, terminating")
            self.__worker.terminate()

            return True

        if exit_code != 0:
            print(f"WARN: Process exited abnormally with code: {exit_code}")
        else:
            print("INFO: Process exited normally")

        return True
