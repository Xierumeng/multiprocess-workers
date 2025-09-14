"""
Queue.
"""

import multiprocessing.managers

from . import queue_property_data


class QueueWrapper:
    """
    Wrapper for an underlying queue proxy and other information.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, mp_manager: multiprocessing.managers.SyncManager, queue_property: queue_property_data.QueuePropertyData,
    ) -> tuple[True, "QueueWrapper"] | tuple[False, None]:
        """
        queue_property: Queue property data.
        mp_manager: Python multiprocessing manager.

        Return: Success, object.
        """
        return True, QueueWrapper(cls.__create_key, mp_manager, queue_property)

    def __init__(
        self,
        class_private_create_key: object,
        mp_manager: multiprocessing.managers.SyncManager,
        queue_property: queue_property_data.QueuePropertyData,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is QueueWrapper.__create_key, "Use create() method"

        self.queue_property = queue_property
        self.queue = mp_manager.Queue(queue_property.max_size)
