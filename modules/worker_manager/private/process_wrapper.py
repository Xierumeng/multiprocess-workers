"""
Process.
"""

import inspect
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
        controller: worker_controller.WorkerController,
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
        result = cls.__is_signature_match(
            target_function, target_arguments, input_queues, output_queues
        )
        if not result:
            print(f"ERROR: Failed to create worker process: {target_function}")
            return False, None

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

        # TODO: Start using these
        # pylint: disable=unused-private-member
        self.__worker = worker
        self.__controller = controller
        # pylint: enable=unused-private-member

    @staticmethod
    def __is_signature_match(
        target_function: "(...) -> object",  # type: ignore
        target_arguments: tuple,
        input_queues: list[queue_wrapper.QueueWrapper],
        output_queues: list[queue_wrapper.QueueWrapper],
    ) -> bool:
        """
        Check queue names match function signature.

        target_function: Function.
        target_arguments: Arguments for the function. Can be empty.
        input_queues: Input queues. Can be empty.
        output_queues: Output queues. Can be empty.

        Return: Success.
        """
        argument_length = len(target_arguments)
        input_queues_length = len(input_queues)
        output_queues_length = len(output_queues)
        controller_argument_length = 1

        total_argument_length = (
            argument_length
            + input_queues_length
            + output_queues_length
            + controller_argument_length
        )

        target_signature = inspect.signature(target_function)
        target_parameter_names = list(target_signature.parameters)

        if total_argument_length != len(target_parameter_names):
            print(
                f"ERROR: Argument length does not match function signature: {target_function}: {target_signature}"
            )
            return False

        input_start_index = argument_length
        input_end_index = input_start_index + input_queues_length
        result = ProcessWrapper.__is_queue_names_match(
            input_queues, target_parameter_names[input_start_index:input_end_index]
        )
        if not result:
            print("ERROR: Input queue names do not match function parameters")
            return False

        output_start_index = input_end_index
        output_end_index = output_start_index + output_queues_length
        result = ProcessWrapper.__is_queue_names_match(
            output_queues, target_parameter_names[output_start_index:output_end_index]
        )
        if not result:
            print("ERROR: Output queue names do not match function parameters")
            return False

        return True

    @staticmethod
    def __is_queue_names_match(
        queues: list[queue_wrapper.QueueWrapper], parameter_names: list[str]
    ) -> bool:
        """
        Check queue names match parameter names.

        queues: Queues.
        parameter_names: Slice of the target parameter names.
        """
        if len(queues) != len(parameter_names):
            print(f"ERROR: Length mismatch: {len(queues)} != {len(parameter_names)}")
            return False

        for queue, parameter_name in zip(queues, parameter_names):
            queue_name = queue.queue_property.name

            if queue_name != parameter_name:
                print(
                    f"ERROR: Queue name: {queue_name} does not match expected parameter: {parameter_name}"
                )
                return False

        return True
