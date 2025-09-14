"""
Worker property data.
"""

class WorkerPropertyData:
    """
    Properties about the worker.
    """

    __create_key = object()

    @classmethod
    def create(
        cls,
        count: int,
        target_function: "(...) -> object",  # type: ignore
        target_arguments: tuple,
        input_queue_names: list[str],
        output_queue_names: list[str],
    ) -> tuple[True, "WorkerPropertyData"] | tuple[False, None]:
        """
        count: Number of workers. Must be greater than 0.
        target_function: Function to run. The function signature is expected to be:
            target_function(
                target_arguments[0],
                target_arguments[1],
                ...
                target_arguments[P],
                queue from input_queue_names[0],
                queue from input_queue_names[1],
                ...
                queue from input_queue_names[Q],
                queue from output_queue_names[0],
                queue from output_queue_names[1],
                ...
                queue from output_queue_names[R],
                worker_controller,
            )
            All queues are multiprocessing queues.
        target_arguments: Arguments for the function. Can be empty.
        input_queue_names: Names of the input queues. Can be empty.
        output_queue_names: Names of the output queues. Can be empty.
        """
        if count <= 0:
            print("ERROR: No workers")
            return False, None

        return True, WorkerPropertyData(
            cls.__create_key,
            count,
            target_function,
            target_arguments,
            input_queue_names,
            output_queue_names,
        )

    def __init__(
        self,
        class_private_create_key: object,
        count: int,
        target_function: "(...) -> object",  # type: ignore
        target_arguments: tuple,
        input_queue_names: list[str],
        output_queue_names: list[str],
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is WorkerPropertyData.__create_key, "Use create() method"

        self.count = count
        self.target_function = target_function
        self.target_arguments = target_arguments
        self.input_queue_names = input_queue_names
        self.output_queue_names = output_queue_names
