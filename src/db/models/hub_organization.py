# third party
from sqlalchemy import (
    String,
    DateTime,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

# project
from src.db.base import Base


class HubOrganization(Base):
    __tablename__ = "hub_organization"

    __table_args__ = (
        {"schema": "nsi"},
    )

    hub_org_hash_key: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
    )

    org_id: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True,
    )

    load_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    record_source: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
