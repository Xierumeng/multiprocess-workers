"""
Generator.
"""

from modules.worker_manager import queue_wrapper
from modules.worker_manager import worker_controller


def generator_worker(
    start: int,
    generator_to_multiplier_queue: queue_wrapper.QueueWrapper,
    controller: worker_controller.WorkerController,
) -> None:
    """
    Generates numbers 0-9 (inclusive).

    start: Starting value.

    Input queues:
        None.
    Output queues:
        generator_to_multiplier_queue

    controller: Worker controller.
    """
    end = 10

    i = start % end
    while True:
        print(f"Generator: {i}")

        generator_to_multiplier_queue.queue.put(i)

        i += 1
        i %= end
