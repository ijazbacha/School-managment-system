"""empty message

Revision ID: 7d6d6dcbc538
Revises: 86b5c032f23c
Create Date: 2021-03-06 11:02:47.840721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d6d6dcbc538'
down_revision = '86b5c032f23c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('leave_teacher',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tech_name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('tech_address', sa.String(length=128), nullable=True),
    sa.Column('tech_contact', sa.String(length=64), nullable=True),
    sa.Column('leave_date', sa.DateTime(), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.Column('tech_subject', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], ),
    sa.ForeignKeyConstraint(['tech_subject'], ['subject.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_leave_teacher_email'), 'leave_teacher', ['email'], unique=False)
    op.create_index(op.f('ix_leave_teacher_tech_address'), 'leave_teacher', ['tech_address'], unique=False)
    op.create_index(op.f('ix_leave_teacher_tech_contact'), 'leave_teacher', ['tech_contact'], unique=False)
    op.create_index(op.f('ix_leave_teacher_tech_name'), 'leave_teacher', ['tech_name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_leave_teacher_tech_name'), table_name='leave_teacher')
    op.drop_index(op.f('ix_leave_teacher_tech_contact'), table_name='leave_teacher')
    op.drop_index(op.f('ix_leave_teacher_tech_address'), table_name='leave_teacher')
    op.drop_index(op.f('ix_leave_teacher_email'), table_name='leave_teacher')
    op.drop_table('leave_teacher')
    # ### end Alembic commands ###