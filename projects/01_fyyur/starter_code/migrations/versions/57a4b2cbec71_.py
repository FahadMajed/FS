"""empty message

Revision ID: 57a4b2cbec71
Revises: e54e68b05b80
Create Date: 2020-10-07 18:31:05.426786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57a4b2cbec71'
down_revision = 'e54e68b05b80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Shows',
    sa.Column('startTime', sa.String(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('startTime')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Shows')
    # ### end Alembic commands ###
