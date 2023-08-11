"""Edit resume model

Revision ID: 8d57bfcf501c
Revises: b5ccb3f968b2
Create Date: 2023-08-10 19:22:19.922849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d57bfcf501c'
down_revision: Union[str, None] = 'b5ccb3f968b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('resume_email_key', 'resume', type_='unique')
    op.drop_constraint('resume_phone_key', 'resume', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('resume_phone_key', 'resume', ['phone'])
    op.create_unique_constraint('resume_email_key', 'resume', ['email'])
    # ### end Alembic commands ###