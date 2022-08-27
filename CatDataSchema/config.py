import os

# The sqlalchemy toolkit uses Database urls which follow RFC-1738 protocol to create an engine
# The syntax: dialect+driver://postgres_username:password@host:port/database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://metabase_catwatcher_user:metabase_catwatcher_pw@192.168.1.157:5432/metabase_catwatcher_db",
)
