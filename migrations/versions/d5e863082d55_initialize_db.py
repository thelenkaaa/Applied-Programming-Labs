"""initialize db

Revision ID: d5e863082d55
Revises: 
Create Date: 2022-11-24 17:20:37.612836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5e863082d55'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'jwt',
        sa.Column('token_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(length=300), nullable=False),
        sa.PrimaryKeyConstraint('token_id')
    )
    op.create_table(
        'cars',
        sa.Column('car_id', sa.Integer(), nullable=False),
        sa.Column('mark', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=255), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('transmission', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('car_id')
    )
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=255), nullable=False),
        sa.Column('last_name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=255), nullable=False),
        sa.Column('drive_license', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_table(
        'orders',
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('renttime', sa.DateTime(), nullable=False),
        sa.Column('renttime_start', sa.DateTime(), nullable=False),
        sa.Column('renttime_end', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('car_id', sa.Integer(), nullable=True),
        sa.Column('payment', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['car_id'], ['cars.car_id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('order_id')
    )


def downgrade() -> None:
    op.drop_table('orders')
    op.drop_table('users')
    op.drop_table('cars')
    op.drop_table('jwt')
