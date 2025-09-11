"""
Test queue property.
"""

from modules.worker_manager import worker_manager


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


class TestCreate:
    """
    Test create() method.
    """
    def test_normal(self) -> None:
        """
        Normal.
        """
        name = "abc"
        max_size = 5

        result, queue_property = worker_manager.QueuePropertyData.create(name, max_size)

        assert result
        assert queue_property is not None

    def test_empty_name(self) -> None:
        """
        Empty name.
        """
        name = ""
        max_size = 5

        result, queue_property = worker_manager.QueuePropertyData.create(name, max_size)

        assert not result
        assert queue_property is None

    def test_max_size_zero(self) -> None:
        """
        Zero max_size.
        """
        name = "abc"
        max_size = 0

        result, queue_property = worker_manager.QueuePropertyData.create(name, max_size)

        assert not result
        assert queue_property is None

    def test_max_size_negative(self) -> None:
        """
        Negative max_size.
        """
        name = "abc"
        max_size = -1

        result, queue_property = worker_manager.QueuePropertyData.create(name, max_size)

        assert not result
        assert queue_property is None
