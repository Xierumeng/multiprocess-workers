"""
Process property data.
"""

import inspect

from .. import queue_wrapper


class ProcessPropertyData:
    """
    Properties to start a worker.
    """

    __create_key = object()

    @classmethod
    def create(
        cls,
        target_function: "(...) -> object",  # type: ignore
        target_arguments: tuple,
        input_queues: list[queue_wrapper.QueueWrapper],
        output_queues: list[queue_wrapper.QueueWrapper],
    ) -> tuple[True, "ProcessPropertyData"] | tuple[False, None]:
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

        Return: Success, object.
        """
        result = cls.__is_signature_match(
            target_function, target_arguments, input_queues, output_queues
        )
        if not result:
            print(f"ERROR: Failed to create process property: {target_function}")
            return False, None

        return True, ProcessPropertyData(
            cls.__create_key, target_function, target_arguments, input_queues, output_queues
        )

    def __init__(
        self,
        class_private_create_key: object,
        target_function: "(...) -> object",  # type: ignore
        target_arguments: tuple,
        input_queues: list[queue_wrapper.QueueWrapper],
        output_queues: list[queue_wrapper.QueueWrapper],
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is ProcessPropertyData.__create_key, "Use create() method"

        self.__target_function = target_function
        self.__target_arguments = target_arguments
        self.__input_queues = input_queues
        self.__output_queues = output_queues

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
        result = ProcessPropertyData.__is_queue_names_match(
            input_queues, target_parameter_names[input_start_index:input_end_index]
        )
        if not result:
            print("ERROR: Input queue names do not match function parameters")
            return False

        output_start_index = input_end_index
        output_end_index = output_start_index + output_queues_length
        result = ProcessPropertyData.__is_queue_names_match(
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

    def get_target_function(self) -> "(...) -> object":  # type: ignore
        """
        Return: Target function.
        """
        return self.__target_function

    def get_arguments(self) -> tuple:
        """
        Return: Tuple of all arguments to be passed to the target function, except for the worker controller.
        """
        arguments = (
            self.__target_arguments + tuple(self.__input_queues) + tuple(self.__output_queues)
        )

        return arguments
