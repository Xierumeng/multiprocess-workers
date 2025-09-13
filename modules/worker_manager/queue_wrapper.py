"""
Queue.
"""

import multiprocessing.managers


class QueueWrapper:
    """
    Wrapper for an underlying queue proxy which also stores maxsize.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, mp_manager: multiprocessing.managers.SyncManager, max_size: int
    ) -> "tuple[True, QueueWrapper] | tuple[False, None]":
        """
        mp_manager: Python multiprocessing manager.
        max_size: Maximum number of items the queue can hold.

        Return: Success, object.
        """
        return True, QueueWrapper(cls.__create_key, mp_manager, max_size)

    def __init__(
        self,
        class_private_create_key: object,
        mp_manager: multiprocessing.managers.SyncManager,
        max_size: int,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is QueueWrapper.__create_key, "Use create() method"

        self.queue = mp_manager.Queue(max_size)
        self.max_size = max_size
