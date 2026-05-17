# third party
from types import SimpleNamespace

# project
from src.services.hub_loader import (
    generate_hub_hash_key,
)
from src.services.sat_attrs_loader import (
    generate_hashdiff,
)


def test_hub_key_deterministic():
    """
    Same org_id must always
    generate same HUB hash key.
    """

    org_id = ("1.2.643.5.1.13.13.12.2.21.1540")

    hash_1 = generate_hub_hash_key(org_id)

    hash_2 = generate_hub_hash_key(org_id)

    assert hash_1 == hash_2


def test_hashdiff_changes_on_attribute_change():
    """
    Attribute change must change hashdiff.
    """

    raw_1 = SimpleNamespace(
        full_name="Hospital A",
        short_name="HA",
        ogrn="123",
        inn="456",
        departmental_affiliation_identifier="DEP1",
        date_of_record_creation="2025-01-01",
    )

    raw_2 = SimpleNamespace(
        full_name="Hospital B",  # changed
        short_name="HA",
        ogrn="123",
        inn="456",
        departmental_affiliation_identifier="DEP1",
        date_of_record_creation="2025-01-01",
    )

    address = (
        "Moscow Lenina 1"
    )

    hash_1 = generate_hashdiff(
        raw=raw_1,
        address=address,
    )

    hash_2 = generate_hashdiff(
        raw=raw_2,
        address=address,
    )

    assert hash_1 != hash_2


def test_hashdiff_stable_on_same_data():
    """
    Same business attributes
    must generate same hashdiff.
    """

    raw = SimpleNamespace(
        full_name="Hospital A",
        short_name="HA",
        ogrn="123",
        inn="456",
        departmental_affiliation_identifier="DEP1",
        date_of_record_creation="2025-01-01",
    )

    address = (
        "Moscow Lenina 1"
    )

    hash_1 = generate_hashdiff(
        raw=raw,
        address=address,
    )

    hash_2 = generate_hashdiff(
        raw=raw,
        address=address,
    )

    assert hash_1 == hash_2
