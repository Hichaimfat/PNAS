import os
import sys
from alembic.config import Config
from alembic import command

# Add current dir to path just in case
sys.path.append(os.getcwd())

# Set database URL with password
os.environ["DATABASE_URL"] = "postgresql://postgres:Khelifa89.@db.bmukpqhoexcvdotieiof.supabase.co:5432/postgres"

print("Starting migration...")
try:
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    print("Migration successful!")
except Exception as e:
    print(f"Migration failed: {e}")
    # Print sys.path and imports for debug
    print("Debug Info:")
    import sqlmodel
    print(f"SQLModel file: {sqlmodel.__file__}")
    sys.exit(1)
