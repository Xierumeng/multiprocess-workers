"""
Multiplier.
"""

from modules.worker_manager import queue_wrapper
from modules.worker_manager import worker_controller


def multiplier_worker(
    factor: int,
    generator_to_multiplier_queue: queue_wrapper.QueueWrapper,
    multiplier_to_printer_queue: queue_wrapper.QueueWrapper,
    controller: worker_controller.WorkerController,
) -> None:
    """
    Multiplies the input by a factor.

    factor: Multiplication factor.

    Input queues:
        generator_to_multiplier_queue
    Output queues:
        multiplier_to_printer_queue

    controller: Worker controller.
    """
    while True:
        i = generator_to_multiplier_queue.queue.get()

        product = factor * i

        print(f"Multiplier: {product} = {factor} * {i}")

        multiplier_to_printer_queue.queue.put(product)
