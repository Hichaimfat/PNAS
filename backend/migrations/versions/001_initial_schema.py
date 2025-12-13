"""initial schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2025-12-13 11:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Extensions
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    # Wilayas
    op.create_table('wilayas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nom', sa.VARCHAR(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wilayas_nom'), 'wilayas', ['nom'], unique=True)

    # Specialites
    op.create_table('specialites',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nom', sa.VARCHAR(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_specialites_nom'), 'specialites', ['nom'], unique=True)

    # Medecins
    op.create_table('medecins',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nom_complet', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('specialite', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('wilaya', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('adresse', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('telephone', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('site_web', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('photo_url', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('priorite_pub', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('completude_profil', sa.Float(), nullable=False, server_default=sa.text('0.5')),
        sa.Column('date_derniere_mise_a_jour', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('informations_additionnelles', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_medecins_nom_complet'), 'medecins', ['nom_complet'], unique=False)
    op.create_index(op.f('ix_medecins_specialite'), 'medecins', ['specialite'], unique=False)
    op.create_index(op.f('ix_medecins_wilaya'), 'medecins', ['wilaya'], unique=False)
    
    # GIN Indexes (Manual Op) for Trigram Search
    # Note: Ensure pg_trgm is created in the DB before running this, done at top of upgrade()
    op.create_index('ix_medecins_nom_complet_trgm', 'medecins', ['nom_complet'], postgresql_using='gin', postgresql_ops={'nom_complet': 'gin_trgm_ops'})


def downgrade() -> None:
    op.drop_index('ix_medecins_nom_complet_trgm', table_name='medecins', postgresql_using='gin')
    op.drop_index(op.f('ix_medecins_wilaya'), table_name='medecins')
    op.drop_index(op.f('ix_medecins_specialite'), table_name='medecins')
    op.drop_index(op.f('ix_medecins_nom_complet'), table_name='medecins')
    op.drop_table('medecins')
    op.drop_index(op.f('ix_specialites_nom'), table_name='specialites')
    op.drop_table('specialites')
    op.drop_index(op.f('ix_wilayas_nom'), table_name='wilayas')
    op.drop_table('wilayas')
