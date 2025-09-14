"""
Example.
"""

from modules.worker_manager import queue_property_data
from modules.worker_manager import worker_manager
from modules.worker_manager import worker_property_data
from modules.worker_manager.example.workers import generator_worker
from modules.worker_manager.example.workers import multiplier_worker
from modules.worker_manager.example.workers import printer_worker


def add_queues_to_manager(manager: worker_manager.WorkerManager, queue_max_size: int) -> bool:
    """
    Add queues to the worker manager.

    manager: Worker manager.

    Return: Success.
    """
    result, generator_to_multiplier_queue_property = queue_property_data.QueuePropertyData.create(
        "generator_to_multiplier_queue", queue_max_size
    )
    if not result:
        return False

    # Get Pylance to stop complaining
    assert generator_to_multiplier_queue_property is not None

    result, multiplier_to_printer_queue_property = queue_property_data.QueuePropertyData.create(
        "multiplier_to_printer_queue", queue_max_size
    )
    if not result:
        return False

    # Get Pylance to stop complaining
    assert multiplier_to_printer_queue_property is not None

    queue_properties = [
        generator_to_multiplier_queue_property,
        multiplier_to_printer_queue_property,
    ]

    count_added = manager.add_queues(queue_properties)
    if count_added != len(queue_properties):
        return False

    return True


def add_worker_groups_to_manager(manager: worker_manager.WorkerManager, worker_count: int) -> bool:
    """
    Add worker groups to the worker manager.

    Return: Success.
    """
    result, generator_worker_properties = worker_property_data.WorkerPropertyData.create(
        worker_count,
        generator_worker.generator_worker,
        (5,),
        [],
        ["generator_to_multiplier_queue"],
    )
    if not result:
        return False

    # Get Pylance to stop complaining
    assert generator_worker_properties is not None

    result, multiplier_worker_properties = worker_property_data.WorkerPropertyData.create(
        worker_count,
        multiplier_worker.multiplier_worker,
        (1_000,),
        ["generator_to_multiplier_queue"],
        ["multiplier_to_printer_queue"],
    )
    if not result:
        return False

    # Get Pylance to stop complaining
    assert multiplier_worker_properties is not None

    result, printer_worker_properties = worker_property_data.WorkerPropertyData.create(
        worker_count,
        printer_worker.printer_worker,
        ("Received: ", " from multipier!"),
        ["multiplier_to_printer_queue"],
        [],
    )
    if not result:
        return False

    # Get Pylance to stop complaining
    assert printer_worker_properties is not None

    worker_properties = [
        generator_worker_properties,
        multiplier_worker_properties,
        printer_worker_properties,
    ]

    count_added = manager.add_worker_groups(worker_properties)
    if count_added != len(worker_properties):
        return False

    return True


def main() -> int:
    """
    Main function.
    """
    queue_max_size = 5
    worker_count_per_group = 2

    result, manager = worker_manager.WorkerManager.create(queue_max_size)
    if not result:
        return -1

    # Get Pylance to stop complaining
    assert manager is not None

    result = add_queues_to_manager(manager, queue_max_size)
    if not result:
        return -1

    result = add_worker_groups_to_manager(manager, worker_count_per_group)
    if not result:
        return -1

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
