"""
Test queue property.
"""

from modules.worker_manager import worker_property_data


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


def stub() -> None:
    """
    Stub function.
    """


class TestCreate:
    """
    Test create() method.
    """

    def test_normal(self) -> None:
        """
        Normal.
        """
        count = 5

        result, worker_property = worker_property_data.WorkerPropertyData.create(
            count, stub, (), [], []
        )

        assert result
        assert worker_property is not None

    def test_count_zero(self) -> None:
        """
        Zero max_size.
        """
        count = 0

        result, worker_property = worker_property_data.WorkerPropertyData.create(
            count, stub, (), [], []
        )

        assert not result
        assert worker_property is None

    def test_count_negative(self) -> None:
        """
        Negative max_size.
        """
        count = -1

        result, worker_property = worker_property_data.WorkerPropertyData.create(
            count, stub, (), [], []
        )

        assert not result
        assert worker_property is None
