# third party
import hashlib
from sqlalchemy import select
from sqlalchemy.orm import Session

# project
from src.db.models.raw_medical_organization import (
    RawMedicalOrganization,
)
from src.db.models.hub_organization import (
    HubOrganization,
)
from src.config.settings import RECORD_SOURCE
from src.logger import logger


def generate_hub_hash_key(oid: str) -> str:
    """
    Generates HUB hash key from business key (oid).
    """

    return hashlib.sha256(
        oid.encode()
    ).hexdigest()


def load_hub_organizations(session: Session) -> None:
    """
    Loads unique organizations from RAW layer
    into HUB table.

    Business key:
        oid

    Rules:
    - one oid = one HUB record
    - duplicates are ignored
    """

    # get all unique OIDs
    query = (
        select(
            RawMedicalOrganization.oid,
        )
        .distinct()
        .where(
            RawMedicalOrganization.oid.is_not(None)
        )
    )

    result = session.execute(query)

    unique_oids = result.scalars().all()

    inserted = 0

    # insert new HUB records
    for oid in unique_oids:

        hub_org_hash_key = generate_hub_hash_key(
            oid
        )

        # check existing HUB record
        existing = session.get(
            HubOrganization,
            hub_org_hash_key,
        )

        if existing:
            continue

        hub_record = HubOrganization(
            hub_org_hash_key=hub_org_hash_key,
            org_id=oid,
            record_source=RECORD_SOURCE,
        )

        session.add(hub_record)

        inserted += 1

    session.commit()

    logger.info(
        f"HUB organizations inserted: {inserted}"
    )
