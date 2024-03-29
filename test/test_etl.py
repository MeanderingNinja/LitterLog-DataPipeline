# assume our test dbs are set up appropriately
# with ENV VARS DATABASE_URL and TESTDATA_DATABASE_URL
"""
20220909
Test to see if data from the target csv file can be loaded to the
database peroperly through the ETL pipeline.
The function that is being tested is pipeline_data()- the extract-transform-load process(ETL).

The function file_watcher() can not be tested at this point
because it has a while loop in it. This will run in a loop and never completes
if there is no error. In this case, our unit test will never complete.

Currently, this is tested using the actual DATABASE_URL, thus tested
on the actual database metbase_catwatcher_db under the role database_catwatcher_user.
This is because the DATABASE_URL is used in the tested funtion pipeline_data().
Ideally, the test is done using the test database pa-test using TEST_DATABASE_URL.

Run the following docker command to setup engine:
`docker run -d --rm -e "POSTGRES_USER=test" -e "POSTGRES_PASSWORD=test" -e "POSTGRES_DB=test" --name cat_data_schema_test_db -p 28444:5432 postgres`
TEST_DATABASE_URL should be set up as "postgresql+psycopg2://test:test@localhost:28444/test"
"""

from pathlib import Path

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text

from CatDataSchema.etl import (
    pipeline_data,
)
from CatDataSchema.models import (
    CatData,
)
from CatDataSchema.config import DATABASE_URL


def test_file_watcher():
    """
    Test to move old data into the new format
    """

    print("Transforming data from csv file and load into test database")
    # pipeline_data(Path("test/data/Atty20220908_20:56:08"))

    #print(f"DATABASE_URL is {DATABASE_URL}")

    test_engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=test_engine)
    with Session.begin() as session:
        # cat_data_record = (
        #     session.query(text('cat_data_schema.cat_litterbox_time_data')).filter(text("cat_data_schema.cat_litterbox_time_data.id = '2022-09-07'")).one()
        # )
        cat_data_record = (
            session.query(text('cat_data_schema.cat_litterbox_time_data'))
            .from_statement(text("SELECT * FROM cat_data_schema.cat_litterbox_time_data WHERE date = '2022-09-07'"))
            .one()
        )

        print(f"cat_data_record is {cat_data_record}")
        assert cat_data_record is not None
test_file_watcher()
        