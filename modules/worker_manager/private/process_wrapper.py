"""
Process.
"""

import multiprocessing as mp

from .. import queue_wrapper
from .. import worker_controller


class ProcessWrapper:
    """
    Wrapper for an underlying process and other information.
    """

    __create_key = object()

    @classmethod
    def create(
        cls,
        target_function: "(...) -> object",  # type: ignore
        target_arguments: tuple,
        input_queues: list[queue_wrapper.QueueWrapper],
        output_queues: list[queue_wrapper.QueueWrapper],
        controller: worker_controller.WorkerController
    ) -> tuple[True, "ProcessWrapper"] | tuple[False, None]:
        """
        target_function: Function to run. The function signature is expected to be:
            target_function(
                target_arguments[0],
                target_arguments[1],
                ...
                target_arguments[P],
                input_queues[0],
                input_queues[1],
                ...
                input_queues[Q],
                output_queues[0],
                output_queues[1],
                ...
                output_queues[R],
                worker_controller,
            )
        target_arguments: Arguments for the function. Can be empty.
        input_queues: Input queues. Can be empty.
        output_queues: Output queues. Can be empty.
        controller: Worker controller.

        Return: Success, object.
        """
        args = target_arguments + tuple(input_queues) + tuple(output_queues) + (controller,)

        try:
            worker = mp.Process(target=target_function, args=args)
        # Catching all exceptions for library call
        # pylint: disable-next=broad-exception-caught
        except Exception as e:
            print(f"ERROR: Failed to create worker process: {e}")
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
