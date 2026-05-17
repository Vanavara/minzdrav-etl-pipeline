# third party
from sqlalchemy import (
    BigInteger,
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


class SatOrganizationChanges(Base):
    __tablename__ = "sat_organization_changes"

    __table_args__ = (
        {"schema": DB_SCHEMA},
    )

    change_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True,)
    loaded_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(),)
    hub_org_hash_key: Mapped[str] = mapped_column(String(64),ForeignKey(
            f"{DB_SCHEMA}.hub_organization.hub_org_hash_key"), nullable=False,
    )
    attribute_name: Mapped[str] = mapped_column(Text, nullable=False,)
    attribute_value: Mapped[str | None] = mapped_column(Text, )
    valid_from: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False,)
    valid_to: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True,)
