"""change_to_my_model_lowercase

Revision ID: cfa0ebc93b1e
Revises: 6f9eca4d213f
Create Date: 2022-08-02 15:49:02.529297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfa0ebc93b1e'
down_revision = '6f9eca4d213f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cat_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('entry', sa.DateTime(), nullable=True),
    sa.Column('depart', sa.DateTime(), nullable=True),
    sa.Column('duration', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cat_data')
    # ### end Alembic commands ###