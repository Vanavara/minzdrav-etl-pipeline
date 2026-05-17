# third party
import hashlib
from datetime import timedelta
from typing import Callable
from sqlalchemy import select
from sqlalchemy.orm import Session

# project
from src.db.models.raw_medical_organization import RawMedicalOrganization
from src.db.models.sat_organization_changes import SatOrganizationChanges
from src.config.settings import BATCH_SIZE
from src.logger import logger


def generate_hub_hash_key(oid: str) -> str:
    return hashlib.sha256(
        oid.encode()
    ).hexdigest()


def build_address(raw: RawMedicalOrganization) -> str:
    return " ".join(
        filter(
            None,
            [
                raw.region_name,
                raw.settlement_prefix,
                raw.settlement_name,
                raw.street_prefix,
                raw.street_name,
                raw.house_number,
            ],
        )
    )


TRACKED_ATTRIBUTES: dict[str, Callable[[RawMedicalOrganization], str | None]] = {
    "full_name": lambda raw: raw.full_name,
    "short_name": lambda raw: raw.short_name,
    "inn": lambda raw: raw.inn,
    "ogrn": lambda raw: raw.ogrn,
    "address": build_address,
    "ved_affiliation_id": lambda raw: raw.departmental_affiliation_identifier,
}


def load_sat_organization_changes(
    session: Session,
    source_version: str,
) -> None:
    """
    Loads attribute-level history into nsi.sat_organization_changes.

    Optimized version:
    - loads active changes once;
    - avoids SQL query inside loop;
    - inserts new rows in batches;
    - updates old active rows in memory.
    """

    raw_records = (
        session.execute(
            select(RawMedicalOrganization)
            .where(
                RawMedicalOrganization.source_version == source_version
            )
        )
        .scalars()
        .all()
    )

    active_changes = (
        session.execute(
            select(SatOrganizationChanges)
            .where(
                SatOrganizationChanges.valid_to.is_(None)
            )
        )
        .scalars()
        .all()
    )

    active_lookup = {
        (
            row.hub_org_hash_key,
            row.attribute_name,
        ): row
        for row in active_changes
    }

    new_records: list[SatOrganizationChanges] = []

    inserted = 0
    closed = 0
    processed = 0

    for raw in raw_records:
        if not raw.oid:
            continue

        hub_org_hash_key = generate_hub_hash_key(
            raw.oid
        )

        # valid_from = raw.loaded_at.date()
        valid_from = raw.loaded_at

        for attribute_name, value_getter in TRACKED_ATTRIBUTES.items():
            new_value = value_getter(raw)

            lookup_key = (
                hub_org_hash_key,
                attribute_name,
            )

            active_change = active_lookup.get(
                lookup_key
            )

            # first value for this attribute
            if active_change is None:
                new_change = SatOrganizationChanges(
                    hub_org_hash_key=hub_org_hash_key,
                    attribute_name=attribute_name,
                    attribute_value=new_value,
                    valid_from=valid_from,
                    valid_to=None,
                )

                new_records.append(new_change)
                active_lookup[lookup_key] = new_change

                inserted += 1
                processed += 1

            # value did not change
            elif active_change.attribute_value == new_value:
                processed += 1
                continue

            # value changed
            else:
                active_change.valid_to = valid_from - timedelta(microseconds=1)

                new_change = SatOrganizationChanges(
                    hub_org_hash_key=hub_org_hash_key,
                    attribute_name=attribute_name,
                    attribute_value=new_value,
                    valid_from=valid_from,
                    valid_to=None,
                )

                new_records.append(new_change)
                active_lookup[lookup_key] = new_change

                inserted += 1
                closed += 1
                processed += 1

            if len(new_records) >= BATCH_SIZE:
                session.bulk_save_objects(new_records)
                session.commit()

                logger.info(
                    f"SAT CHANGES processed: {processed}, "
                    f"inserted: {inserted}, "
                    f"closed: {closed}"
                )

                new_records.clear()

    if new_records:
        session.bulk_save_objects(new_records)
        session.commit()

    logger.info(
        f"SAT CHANGES inserted: {inserted}, closed: {closed}"
    )
