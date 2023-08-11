"""Edit resume model

Revision ID: 53c2be26af85
Revises: 30f073fd02b7
Create Date: 2023-08-11 17:14:51.735359

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53c2be26af85'
down_revision: Union[str, None] = '30f073fd02b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('resume_file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resume',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_resume_file', sa.Integer(), nullable=False),
    sa.Column('fio', sa.String(), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('gender', sa.Enum('man', 'woman', 'none', name='gender'), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('education', sa.Enum('postgraduate_study', 'magistracy', 'specialty', 'bachelor_course', 'bachelor', 'average_first', 'average_second', 'average_general', 'basic_general', 'none', name='education'), nullable=False),
    sa.Column('experience', sa.Integer(), nullable=False),
    sa.Column('profession', sa.ARRAY(sa.String()), nullable=False),
    sa.ForeignKeyConstraint(['id_resume_file'], ['resume_file.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('resume')
    op.drop_table('resume_file')
    # ### end Alembic commands ###