"""updated order table

Revision ID: c45e474faeeb
Revises: a8236a99f5d2
Create Date: 2023-06-07 22:33:33.970728

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = 'c45e474faeeb'
down_revision = 'a8236a99f5d2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'orders',
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('car_id', sa.Integer(), nullable=True),
        sa.Column('country', sa.String(length=20), nullable=False),
        sa.Column('city', sa.String(length=20), nullable=False),
        sa.Column('address', sa.String(length=20), nullable=False),
        sa.Column('amount_days', sa.Integer(), nullable=False),
        sa.Column('color', sa.String(length=20), nullable=False),
        sa.Column('renttime', sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(['car_id'], ['cars.car_id'], name='orders_ibfk_1'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='orders_ibfk_2'),
        sa.PrimaryKeyConstraint('order_id'),
        mysql_collate='utf8mb4_0900_ai_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'

    )

def downgrade() -> None:
    op.drop_table('orders')