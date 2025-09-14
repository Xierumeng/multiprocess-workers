"""
Printer.
"""

from modules.worker_manager import queue_wrapper
from modules.worker_manager import worker_controller


def printer_worker(
    prefix: str,
    suffix: str,
    multiplier_to_printer_queue: queue_wrapper.QueueWrapper,
    controller: worker_controller.WorkerController,
) -> None:
    """
    Prints with prefix and suffix.

    prefix: Prefix.
    suffix: Suffix.

    Input queues:
        multiplier_to_printer_queue
    Output queues:
        None.

    controller: Worker controller.
    """
    while True:
        i = multiplier_to_printer_queue.queue.get()

        print_str = prefix + str(i) + suffix

        print(f"Printer: {print_str}")
