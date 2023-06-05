import os
from dotenv import load_dotenv


# The sqlalchemy toolkit uses Database urls which follow RFC-1738 protocol to create an engine
# The syntax: dialect+driver://postgres_username:password@host:port/database


# To run the project through Jenkins, modify the DABABASE_URL to
# "postgresql+psycopg2://metabase_catwatcher_test_user:metabase_catwatcher_test_pw@db:5432/metabase_catwatcher_test_db"

# 20230227: can use f"postgresql+psycopg2://pa-test:pa-test@192.168.1.157:5432/pa-test?options=-csearch_path%3D{SCHEMA_NAME} to specify the schema
load_dotenv()
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://metabase_catwatcher_user:metabase_catwatcher_pw@192.168.1.157:5432/metabase_catwatcher_db",
)

# 20230221: I didn't change the DATABASE_URL last time (3 days ago) I ran Jenkins build and it still worked though. Go figure out why later.
