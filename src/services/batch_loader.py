# third party
from sqlalchemy.orm import Session

# project
from src.db.models.raw_medical_organization import (
    RawMedicalOrganization,
)


def insert_batch(
    session: Session,
    records: list[dict],
) -> None:

    objects = [
        RawMedicalOrganization(**record)
        for record in records
    ]

    session.bulk_save_objects(objects)

    session.commit()
