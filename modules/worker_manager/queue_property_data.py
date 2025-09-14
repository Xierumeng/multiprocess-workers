"""
Queue property data.
"""


class QueuePropertyData:
    """
    Properties about the queue.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, name: str, max_size: int
    ) -> tuple[True, "QueuePropertyData"] | tuple[False, None]:
        """
        name: Name of the queue. Must not be empty string.
        max_size: Maximum number of items that can be held in the queue. Must be greater than 0.

        Return: Success, object.
        """
        if name == "":
            print("ERROR: Name cannot be empty")
            return False, None

        if max_size <= 0:
            print("ERROR: Queue max size must be greater than 0")
            return False, None

        return True, QueuePropertyData(cls.__create_key, name, max_size)

    def __init__(self, class_private_create_key: object, name: str, max_size: int) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is QueuePropertyData.__create_key, "Use create() method"

        self.name = name
        self.max_size = max_size
