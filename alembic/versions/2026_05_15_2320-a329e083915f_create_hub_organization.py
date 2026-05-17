"""create hub organization

Revision ID: a329e083915f
Revises: d0f3b031a452
Create Date: 2026-05-15 23:20:26.480016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a329e083915f'
down_revision: Union[str, Sequence[str], None] = 'd0f3b031a452'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hub_organization",

        sa.Column("hub_org_hash_key",sa.String(length=64),nullable=False,),
        sa.Column("org_id",sa.Text(),nullable=False,),
        sa.Column( "load_date",sa.DateTime(timezone=True),server_default=sa.text("now()"),nullable=False,),
        sa.Column("record_source",sa.Text(),nullable=False,),

        sa.PrimaryKeyConstraint( "hub_org_hash_key"),
        sa.UniqueConstraint( "org_id"),

        schema="nsi",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_table('hub_organization', schema='nsi')
    # ### end Alembic commands ###
