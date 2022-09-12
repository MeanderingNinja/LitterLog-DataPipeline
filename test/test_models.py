"""
Emma 20220909
pytest to verify each column has the correct datatype and data can be uploaded to the database.

Ran python3 -m pytest test/test_models.py -v: Both passes.
To see if the table and data are indeed in the database, I removed the clean up code after yield.
cat_data table showed up, however, I don't see any data populated there.
"""
import os
from unittest import mock
import pytest
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, select, delete
from sqlalchemy import inspect
from CatDataSchema.models import (
    CatData,
    Base,
)
from datetime import date, datetime


# The env var is not set 20220908
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg2://pa-test:pa-test@192.168.1.157:5432/pa-test",
)

# The scope is set to "session" to inform pytest that we want 
# the fixture to be destroyed at the end of the test session.
@pytest.fixture(scope="session")
def engine():
    return create_engine(TEST_DATABASE_URL)


@pytest.fixture(scope="session")
def tables(engine):
    """
    Create tables once
    """
    Base.metadata.create_all(engine)
    # returns None, the same as a Return with no parameter
    # can't be removed as it pauses the operation of a generator and returns control to the calling function
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
        id = 1,
        date = date.today(),
        entry = datetime.fromtimestamp(1661315366.0901508),  # Probably need to the transformed datatype like what I did in ETL
        depart = datetime.fromtimestamp(1661315458.6241393),
        duration = 92.53398847579956
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


