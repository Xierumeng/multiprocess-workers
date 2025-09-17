"""
Process.
"""

import multiprocessing as mp

from . import process_property_data
from .. import worker_controller


class ProcessWrapper:
    """
    Wrapper for an underlying process and other information.
    """

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

        # TODO: Start using these
        # pylint: disable=unused-private-member
        self.__worker = worker
        self.__controller = controller
        # pylint: enable=unused-private-member
