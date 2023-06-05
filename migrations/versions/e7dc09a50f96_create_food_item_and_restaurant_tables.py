"""Create food_item and restaurant tables

Revision ID: e7dc09a50f96
Revises: 
Create Date: 2023-06-04 13:53:52.384427

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e7dc09a50f96'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Ignore first migration
    return
    # ### end Alembic commands ###


def downgrade():
    # Ignore first migration
    return
    # ### end Alembic commands ###
