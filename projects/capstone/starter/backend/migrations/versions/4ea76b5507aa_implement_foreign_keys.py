"""Implement Foreign Keys

Revision ID: 4ea76b5507aa
Revises: 34961b814fc6
Create Date: 2021-08-08 14:39:15.295532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ea76b5507aa'
down_revision = '34961b814fc6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('classroom_cls_crs_id_fkey',
                       'classroom', type_='foreignkey')
    op.drop_column('classroom', 'cls_crs_id')
    op.add_column('course', sa.Column(
        'crs_lec_id', sa.Integer(), nullable=False))
    op.add_column('course', sa.Column(
        'crs_cls_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'course', 'classroom',
                          ['crs_cls_id'], ['cls_id'])
    op.create_foreign_key(None, 'course', 'lecturer',
                          ['crs_lec_id'], ['lec_id'])
    op.drop_constraint('lecturer_lec_crs_id_fkey',
                       'lecturer', type_='foreignkey')
    op.drop_column('lecturer', 'lec_crs_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lecturer', sa.Column(
        'lec_crs_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('lecturer_lec_crs_id_fkey',
                          'lecturer', 'course', ['lec_crs_id'], ['crs_id'])
    op.drop_constraint(None, 'course', type_='foreignkey')
    op.drop_constraint(None, 'course', type_='foreignkey')
    op.drop_column('course', 'crs_cls_id')
    op.drop_column('course', 'crs_lec_id')
    op.add_column('classroom', sa.Column(
        'cls_crs_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('classroom_cls_crs_id_fkey',
                          'classroom', 'course', ['cls_crs_id'], ['crs_id'])
    # ### end Alembic commands ###