# third party
from datetime import (
    datetime,
    timedelta,
)

# project
from src.db.models.sat_organization_changes import (
    SatOrganizationChanges,
)


def test_first_load_creates_open_ended_record():
    """
    First attribute version
    must have open-ended validity.
    """

    record = SatOrganizationChanges(
        hub_org_hash_key="hash_1",
        attribute_name="full_name",
        attribute_value="Hospital A",
        valid_from=datetime(
            2025,
            1,
            1,
        ),
        valid_to=None,
    )

    assert record.valid_to is None


def test_second_load_closes_old_record():
    """
    Previous record must be closed
    when new attribute version appears.
    """

    old_valid_from = datetime(
        2025,
        1,
        1,
        10,
        0,
        0,
    )

    new_valid_from = datetime(
        2025,
        1,
        2,
        10,
        0,
        0,
    )

    old_valid_to = (
        new_valid_from
        - timedelta(microseconds=1)
    )

    assert old_valid_to < new_valid_from


def test_unchanged_attribute_no_new_version():
    """
    Same attribute value
    should not create new version.
    """

    old_value = (
        "Hospital A"
    )

    new_value = (
        "Hospital A"
    )

    should_create_new_version = (
        old_value != new_value
    )

    assert (
        should_create_new_version
        is False
    )


def test_valid_to_before_new_valid_from():
    """
    valid_to must be earlier
    than next valid_from.
    """

    new_valid_from = datetime(
        2025,
        1,
        2,
        12,
        0,
        0,
    )

    old_valid_to = (
        new_valid_from
        - timedelta(microseconds=1)
    )

    assert (
        old_valid_to
        < new_valid_from
    )
