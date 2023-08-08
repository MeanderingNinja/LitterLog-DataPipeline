"""
pytest to verify each column has the correct datatype and data can be uploaded to the database.

Run the following docker command to setup engine:
`docker run -d --rm -e "POSTGRES_USER=test" -e "POSTGRES_PASSWORD=test" -e "POSTGRES_DB=test" --name cat_data_schema_test_db -p 28444:5432 postgres`
TEST_DATABASE_URL should be set up as "postgresql+psycopg2://test:test@localhost:28444/test"

Run the following command to test:
`python3 -m pytest test/test_models.py -v`

Run the following command to manually check if the table and data are in the database (Remove the clean up code after yield before checking):
`psql -h localhost -p 28444 -U test -d test`

(The table showed up, however, I don't see any data populated there.)
"""

import os
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy import inspect
import pytest
from CatDataSchema.models import (
    CatData,
    Base,
)


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg2://test:test@localhost:28444/test",
)


@pytest.fixture(scope="session")
def engine():
    return create_engine(TEST_DATABASE_URL)


@pytest.fixture(scope="session")
def tables(engine):
    """
    Create schema and table once.
    """
    schema_name = "cat_data_schema"
    with engine.connect() as conn:
        if not conn.dialect.has_schema(conn, schema_name):
            conn.execute(CreateSchema(schema_name))
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def dbsession(engine, tables):
    """
    Returns an sqlalchemy session, and after the test tears down everything properly
    """
    inspector = inspect(engine)
    print(inspector.get_table_names())  # engine.table_names() method is deprecated
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def mock_cat_data():
    cat_data_entry = CatData(
        id=1,
        date=date.today(),
        entry=datetime.fromtimestamp(
            1661315366.0901508
        ),  # Probably need to the transformed datatype like what I did in ETL
        depart=datetime.fromtimestamp(1661315458.6241393),
        duration=92.53398847579956,
    )
    return cat_data_entry


def test_data_types(mock_cat_data):
    """
    Verify entry in each column has the correct datatype.
    """
    assert isinstance(mock_cat_data.id, int)
    assert isinstance(mock_cat_data.date, date)
    assert isinstance(mock_cat_data.entry, datetime)
    assert isinstance(mock_cat_data.depart, datetime)
    assert isinstance(mock_cat_data.duration, float)


def test_dbsession(dbsession, mock_cat_data):
    """
    Verify that data can be uploaded to the database.
    """
    dbsession.add_all([mock_cat_data])
    dbsession.commit()
    dbsession.flush()
