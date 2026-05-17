# project
from src.utils.dates import parse_date
import hashlib


def map_record(record: dict, source_version: str) -> dict:

    oid = record.get("oid")

    raw_hash_key = hashlib.sha256(
        f"{oid}|{source_version}".encode()
    ).hexdigest()

    return {
        "raw_hash_key": raw_hash_key,
        "source_version": source_version,
        "raw_data": record,
        "unique_id": str(record.get("id")) if record.get("id") else None,
        "oid": record.get("oid"),
        "full_name": record.get("nameFull"),
        "short_name": record.get("nameShort"),
        "healthcare_system_entity_code": (
            str(record.get("medicalSubjectId"))
            if record.get("medicalSubjectId") is not None
            else None
        ),
        "healthcare_system_entity_name": (
            record.get("medicalSubjectName")
        ),
        "inn": record.get("inn"),
        "kpp": record.get("kpp"),
        "ogrn": record.get("ogrn"),
        "region_rf_code": (
            str(record.get("regionId"))
            if record.get("regionId") is not None
            else None
        ),
        "region_rf_name": record.get("regionName"),
        "ownership_form": (
            str(record.get("organizationType"))
            if record.get("organizationType") is not None
            else None
        ),

        "departmental_affiliation_identifier": (
            str(record.get("moDeptId"))
            if record.get("moDeptId") is not None
            else None
        ),

        "departmental_affiliation": (
            record.get("moDeptName")
        ),

        "founder": record.get("founder"),

        "date_of_record_deletion": parse_date(
            record.get("deleteDate")
        ),

        "reason_of_record_deletion": (
            record.get("deleteReason")
        ),

        "date_of_record_creation": parse_date(
            record.get("createDate")
        ),

        "last_modification_date": parse_date(
            record.get("modifyDate")
        ),

        "organization_level": record.get("moLevel"),

        "activity_type_identifier": (
            str(record.get("moAgencyKindId"))
            if record.get("moAgencyKindId") is not None
            else None
        ),

        "activity_type": record.get("moAgencyKind"),

        "zip_code": record.get("postIndex"),

        "latitude": (
            float(record["latitude"])
            if record.get("latitude")
            else None
        ),

        "longitude": (
            float(record["longtitude"])
            if record.get("longtitude")
            else None
        ),

        "locality_identifier": record.get("aoidArea"),
        "street_identifier": record.get("aoidStreet"),
        "house_identifier": record.get("houseid"),

        "region_code": (
            str(record.get("addrRegionId"))
            if record.get("addrRegionId") is not None
            else None
        ),

        "region_name": record.get("addrRegionName"),

        "settlement_name": record.get("areaName"),
        "settlement_prefix": record.get("prefixArea"),

        "street_name": record.get("streetName"),
        "street_prefix": record.get("prefixStreet"),

        "house_number": record.get("house"),
    }
