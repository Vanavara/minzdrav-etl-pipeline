# third party
from sqlalchemy import (
    String,
    Text,
    Date,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

# project
from src.db.base import Base
from src.config.settings import DB_SCHEMA


class SatOrganizationAttrs(Base):
    __tablename__ = "sat_organization_attrs"

    __table_args__ = (
        {"schema": DB_SCHEMA},
    )

    hub_org_hash_key: Mapped[str] = mapped_column(String(64),ForeignKey("nsi.hub_organization.hub_org_hash_key"),
        primary_key=True,
    )
    hashdiff: Mapped[str] = mapped_column(String(64),primary_key=True,)
    load_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(),)
    full_name: Mapped[str | None] = mapped_column(Text)
    short_name: Mapped[str | None] = mapped_column(Text)
    ogrn: Mapped[str | None] = mapped_column(Text)
    inn: Mapped[str | None] = mapped_column(Text)
    address: Mapped[str | None] = mapped_column(Text)
    ved_affiliation_id: Mapped[str | None] = mapped_column(Text)
    inclusion_date: Mapped[Date | None] = mapped_column(Date)
    record_source: Mapped[str] = mapped_column(Text, nullable=False,)
