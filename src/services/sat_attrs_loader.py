# third party
import hashlib
from sqlalchemy import (
    select,
    and_,
)
from sqlalchemy.orm import Session

# project
from src.db.models.raw_medical_organization import (
    RawMedicalOrganization,
)
from src.db.models.sat_organization_attrs import (
    SatOrganizationAttrs,
)
from src.config.settings import (
    RECORD_SOURCE,
    BATCH_SIZE
)
from src.logger import logger


def generate_hub_hash_key(oid: str) -> str:
    """
    Generates HUB hash key from oid.
    """

    return hashlib.sha256(
        oid.encode()
    ).hexdigest()


def build_address(
    raw: RawMedicalOrganization,
) -> str:
    """
    Builds full address string.
    """

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


def generate_hashdiff(
    raw: RawMedicalOrganization,
    address: str,
) -> str:
    """
    Generates satellite hashdiff.

    Only business descriptive attributes
    are included.
    """

    hash_source = "|".join(
        [
            raw.full_name or "",
            raw.short_name or "",
            raw.ogrn or "",
            raw.inn or "",
            address or "",
            raw.departmental_affiliation_identifier or "",
            str(raw.date_of_record_creation or ""),
        ]
    )

    return hashlib.sha256(
        hash_source.encode()
    ).hexdigest()


def load_sat_organization_attrs(
    session: Session,
) -> None:
    """
    Loads organization attributes satellite.

    Optimized version:
    - preload existing hashdiffs;
    - no SQL inside loop;
    - streaming RAW loading;
    - batch inserts.
    """

    # preload existing satellite keys
    existing_rows = (
        session.execute(
            select(
                SatOrganizationAttrs.hub_org_hash_key,
                SatOrganizationAttrs.hashdiff,
            )
        )
        .all()
    )

    existing_lookup = set(
        existing_rows
    )

    # stream RAW records
    raw_records = (
        session.execute(
            select(
                RawMedicalOrganization
            )
        )
        .scalars()
        .yield_per(5000)
    )

    new_records: list[
        SatOrganizationAttrs
    ] = []

    inserted = 0
    processed = 0

    # process RAW records
    for raw in raw_records:

        if not raw.oid:
            continue

        # HUB hash key
        hub_org_hash_key = (
            generate_hub_hash_key(
                raw.oid
            )
        )

        # build address
        address = build_address(raw)

        # generate hashdiff
        hashdiff = generate_hashdiff(
            raw=raw,
            address=address,
        )

        lookup_key = (
            hub_org_hash_key,
            hashdiff,
        )

        # skip existing version
        if lookup_key in existing_lookup:
            processed += 1
            continue

        # create satellite row
        satellite = (
            SatOrganizationAttrs(
                hub_org_hash_key=hub_org_hash_key,
                hashdiff=hashdiff,

                full_name=raw.full_name,
                short_name=raw.short_name,

                ogrn=raw.ogrn,
                inn=raw.inn,

                address=address,

                ved_affiliation_id=(
                    raw.departmental_affiliation_identifier
                ),

                inclusion_date=(
                    raw.date_of_record_creation
                ),

                record_source=RECORD_SOURCE,
            )
        )

        new_records.append(
            satellite
        )

        existing_lookup.add(
            lookup_key
        )

        inserted += 1
        processed += 1

        # batch insert
        if len(new_records) >= BATCH_SIZE:

            session.bulk_save_objects(
                new_records
            )

            session.commit()

            logger.info(
                f"SAT ATTRS processed: "
                f"{processed}, "
                f"inserted: {inserted}"
            )

            new_records.clear()

    # final batch insert
    if new_records:

        session.bulk_save_objects(
            new_records
        )

        session.commit()

    logger.info(
        f"SAT ATTRS inserted: "
        f"{inserted}"
    )
