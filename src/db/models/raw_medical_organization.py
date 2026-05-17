# third party
from sqlalchemy import (
    String,
    Date,
    DateTime,
    Float,
    Index,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

# project
from src.db.base import Base
from src.config.settings import DB_SCHEMA


class RawMedicalOrganization(Base):
    __tablename__ = "raw_medical_organizations"

    __table_args__ = (
        Index("ix_raw_medical_organizations_oid", "oid"),
        Index("ix_raw_medical_organizations_source_version", "source_version"),
        {"schema": DB_SCHEMA},
    )

    raw_hash_key: Mapped[str] = mapped_column(String(64), primary_key=True,)
    source_version: Mapped[str] = mapped_column(Text, nullable=False,)
    loaded_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False,server_default=func.now(),)
    raw_data: Mapped[dict] = mapped_column(JSONB, nullable=False,)

    unique_id: Mapped[str | None] = mapped_column(Text)
    oid: Mapped[str | None] = mapped_column(Text)
    oid_non_unique: Mapped[str | None] = mapped_column(Text)
    full_name: Mapped[str | None] = mapped_column(Text)
    short_name: Mapped[str | None] = mapped_column(Text)
    unique_parent_id: Mapped[str | None] = mapped_column(Text)
    healthcare_system_entity_code: Mapped[str | None] = mapped_column(Text)
    healthcare_system_entity_name: Mapped[str | None] = mapped_column(Text)
    inn: Mapped[str | None] = mapped_column(Text)
    kpp: Mapped[str | None] = mapped_column(Text)
    ogrn: Mapped[str | None] = mapped_column(Text)
    region_rf_code: Mapped[str | None] = mapped_column(Text)
    region_rf_name: Mapped[str | None] = mapped_column(Text)
    ownership_form: Mapped[str | None] = mapped_column(Text)
    departmental_affiliation_identifier: Mapped[str | None] = mapped_column(Text)
    departmental_affiliation: Mapped[str | None] = mapped_column(Text)
    founder: Mapped[str | None] = mapped_column(Text)
    date_of_record_deletion: Mapped[Date | None] = mapped_column(Date)
    reason_of_record_deletion: Mapped[str | None] = mapped_column(Text)
    date_of_record_creation: Mapped[Date | None] = mapped_column(Date)
    last_modification_date: Mapped[Date | None] = mapped_column(Date)
    organization_level: Mapped[str | None] = mapped_column(Text)
    activity_type_identifier: Mapped[str | None] = mapped_column(Text)
    activity_type: Mapped[str | None] = mapped_column(Text)
    activity_profile_id: Mapped[str | None] = mapped_column(Text)
    activity_profile: Mapped[str | None] = mapped_column(Text)
    zip_code: Mapped[str | None] = mapped_column(Text)
    cadastral_number: Mapped[str | None] = mapped_column(Text)
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    fias_version: Mapped[str | None] = mapped_column(Text)
    locality_identifier: Mapped[str | None] = mapped_column(Text)
    street_identifier: Mapped[str | None] = mapped_column(Text)
    house_identifier: Mapped[str | None] = mapped_column(Text)
    region_code: Mapped[str | None] = mapped_column(Text)
    region_name: Mapped[str | None] = mapped_column(Text)
    okato_region_code: Mapped[str | None] = mapped_column(Text)
    federal_significance_city: Mapped[str | None] = mapped_column(Text)
    settlement_name: Mapped[str | None] = mapped_column(Text)
    settlement_prefix: Mapped[str | None] = mapped_column(Text)
    street_name: Mapped[str | None] = mapped_column(Text)
    street_prefix: Mapped[str | None] = mapped_column(Text)
    house_number: Mapped[str | None] = mapped_column(Text)
    building_number: Mapped[str | None] = mapped_column(Text)
    corpus_number: Mapped[str | None] = mapped_column(Text)
    oid_head_organization_for_sp_1: Mapped[str | None] = mapped_column(Text)
    oid_sp_1: Mapped[str | None] = mapped_column(Text)
    oid_subsidiaries_sp_1: Mapped[str | None] = mapped_column(Text)
