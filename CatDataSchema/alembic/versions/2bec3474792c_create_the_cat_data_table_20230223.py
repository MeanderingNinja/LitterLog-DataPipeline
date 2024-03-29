"""Create the cat_litterbox_time_data Table 20230223

Revision ID: 2bec3474792c
Revises: 
Create Date: 2023-02-23 15:00:45.153898

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "2bec3474792c"
down_revision = None
branch_labels = None
depends_on = None
schema = "cat_data_schema"
table = "cat_litterbox_time_data"


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        table,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("entry", sa.DateTime(), nullable=True),
        sa.Column("depart", sa.DateTime(), nullable=True),
        sa.Column("duration", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema=schema,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table(table, schema=schema)
    # ### end Alembic commands ###
