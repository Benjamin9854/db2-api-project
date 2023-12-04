"""prestamos y BookClient

Revision ID: a8a44353e3e9
Revises: b64a6023f960
Create Date: 2023-12-03 22:06:17.486071

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8a44353e3e9'
down_revision: Union[str, None] = 'b64a6023f960'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('loans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_book', sa.Integer(), nullable=False),
    sa.Column('date_loan', sa.Date(), nullable=False),
    sa.Column('fine', sa.Integer(), nullable=False),
    sa.Column('state', sa.Boolean(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('books', sa.Column('copies', sa.Integer(), nullable=False, server_default='1'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'copies')
    op.drop_table('loans')
    # ### end Alembic commands ###
