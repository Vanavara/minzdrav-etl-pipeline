# third party
import ijson
from sqlalchemy.orm import Session
import hashlib
from sqlalchemy import select

# project
from src.db.session import engine
from src.db.models.raw_medical_organization import RawMedicalOrganization
from src.services.extractor import extract_zip
from src.services.browser_downloader import download_dictionary
from src.services.hub_loader import (load_hub_organizations)
from src.services.sat_attrs_loader import load_sat_organization_attrs
from src.services.sat_changes_loader import load_sat_organization_changes
from src.config.settings import BATCH_SIZE
from src.logger import logger

def parse_date(value: str | None):
    from datetime import datetime

    if not value:
        return None

    return datetime.strptime(value, "%d.%m.%Y").date()


def map_record(record: dict, source_version: str,) -> RawMedicalOrganization:

    oid = record.get("oid")

    raw_hash_key = hashlib.sha256(
        f"{oid}|{source_version}".encode()
    ).hexdigest()


    return RawMedicalOrganization(

        raw_hash_key=raw_hash_key,

        source_version = source_version,
        raw_data=record,

        unique_id=str(record.get("id")) if record.get("id") else None,
        oid=record.get("oid"),
        full_name=record.get("nameFull"),
        short_name=record.get("nameShort"),

        healthcare_system_entity_code=(
            str(record.get("medicalSubjectId"))
            if record.get("medicalSubjectId")
            else None
        ),
        healthcare_system_entity_name=record.get("medicalSubjectName"),

        inn=record.get("inn"),
        kpp=record.get("kpp"),
        ogrn=record.get("ogrn"),

        region_rf_code=(
            str(record.get("regionId"))
            if record.get("regionId")
            else None
        ),
        region_rf_name=record.get("regionName"),

        ownership_form=(
            str(record.get("organizationType"))
            if record.get("organizationType")
            else None
        ),

        departmental_affiliation_identifier=(
            str(record.get("moDeptId"))
            if record.get("moDeptId")
            else None
        ),
        departmental_affiliation=record.get("moDeptName"),

        founder=record.get("founder"),

        date_of_record_deletion=parse_date(record.get("deleteDate")),
        reason_of_record_deletion=record.get("deleteReason"),

        date_of_record_creation=parse_date(record.get("createDate")),
        last_modification_date=parse_date(record.get("modifyDate")),

        organization_level=record.get("moLevel"),

        activity_type_identifier=(
            str(record.get("moAgencyKindId"))
            if record.get("moAgencyKindId")
            else None
        ),
        activity_type=record.get("moAgencyKind"),

        zip_code=record.get("postIndex"),

        latitude=float(record["latitude"])
        if record.get("latitude")
        else None,

        longitude=float(record["longtitude"])
        if record.get("longtitude")
        else None,

        locality_identifier=record.get("aoidArea"),
        street_identifier=record.get("aoidStreet"),
        house_identifier=record.get("houseid"),

        region_code=(
            str(record.get("addrRegionId"))
            if record.get("addrRegionId")
            else None
        ),
        region_name=record.get("addrRegionName"),

        settlement_name=record.get("areaName"),
        settlement_prefix=record.get("prefixArea"),

        street_name=record.get("streetName"),
        street_prefix=record.get("prefixStreet"),

        house_number=record.get("house"),
    )


def main():

    # download dictionary
    zip_path, source_version = download_dictionary(
        version=None,
        # version="6.1998",
        file_format="JSON",
    )


    logger.info(f"ZIP downloaded: {zip_path}")

    # open DB session
    with Session(engine) as session:

        # idempotency check
        existing_version = session.execute(
            select(
                RawMedicalOrganization.raw_hash_key
            ).where(
                RawMedicalOrganization.source_version
                == source_version
            )
        ).first()

        if existing_version:

            logger.info(
                f"Version {source_version} "
                f"already loaded. "
                f"Pipeline skipped."
            )

            return

        # extract ZIP
        extracted_json_path = extract_zip(zip_path)

        logger.info(
            f"JSON extracted: {extracted_json_path}"
        )

        # RAW loading
        batch = []

        with open(
            extracted_json_path,
            "rb",
        ) as file:

            records = ijson.items(
                file,
                "records.item",
            )

            for index, record in enumerate(
                records,
                start=1,
            ):

                organization = map_record(
                    record=record,
                    source_version=source_version,
                )

                batch.append(organization)

                # batch insert
                if len(batch) >= BATCH_SIZE:

                    session.bulk_save_objects(
                        batch
                    )

                    session.commit()

                    logger.info(
                        f"Inserted: {index}"
                    )

                    batch.clear()

            # final batch insert
            if batch:
                session.bulk_save_objects(
                    batch
                )
                session.commit()

                logger.info(
                    f"Final inserted: {index}"
                )

        # HUB loading
        load_hub_organizations(session=session)

        # SAT attrs loading
        load_sat_organization_attrs(session=session)

        # SAT changes loading
        load_sat_organization_changes(session=session, source_version=source_version)

        logger.info(
            "Pipeline completed successfully"
        )


if __name__ == "__main__":
    main()
