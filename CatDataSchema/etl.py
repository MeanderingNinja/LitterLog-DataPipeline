"""
This module contains functions to extract, transform, and load data from csv files of cat data to a PostgreSQL database.
It also includes a file watcher function to monitor a directory for new csv files and triggers the pipeline process.

Functions:

file_watcher(watch_dir: Path)
Monitors the directory specified by watch_dir for csv files and triggers the pipeline process for the last modified file.

pipeline_data(filepath: Path)
The extract-transform-load process for the csv file specified by filepath. Extracts the data from the csv file,
transforms it to match the data types defined in models.py, and loads it into the PostgreSQL database.

"""

import logging
from pathlib import Path
from collections import OrderedDict
from typing import List
from unittest.mock import DEFAULT
import uuid
import csv
from datetime import datetime
import glob
import os
import time

# from CatDataSchema.config import DATABASE_URL
from .config import DATABASE_URL

# from CatDataSchema.models import CatData
from .models import CatData, Base, SCHEMA_NAME, TABLE_NAME
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    create_engine, text
)

LOGGER = logging.getLogger("ETL")
LOGGER.setLevel(logging.INFO)

LOGGER.propagate = False
# create formatter
formatter = logging.Formatter("%(asctime)s :%(levelname)s: %(message)s")

# output on stdout
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# add formatter to stream_handler
stream_handler.setFormatter(formatter)
LOGGER.addHandler(stream_handler)

# 20230313: Output to log file (temp removal, permission issue)-May work on this in the future
# file_handler = logging.FileHandler(filename="/var/log/ETL.log")
# file_handler.setLevel(logging.INFO)
# file_handler.setFormatter(formatter)
# LOGGER.addHandler(file_handler)
DIRECTORY_WATCH_SLEEP = 30
BASE = Base

def file_watcher(watch_dir: Path):
    """
    Checks a given directory for any csv files and triggers a pipeline for the last modified file.
    Assuming there could be multiple csv files in the output directory.
    :Param: watch_dir : Path The directory to be monitored
    """
    last_file_loaded = None
    while True:
        LOGGER.info(f"globbing for existing files in {watch_dir}")

        # Return a list of files that exist in watch_dir
        watch_files = glob.glob(f"{watch_dir}/*")
        ############
        # more detail to be added if there is 0, 1, or more files........
        ############
        times = {}
        for path in watch_files:
            # getmtime: get last modified time
            times[path] = os.path.getmtime(path)
        # Find the file that was last modified
        target_file = max(times, key=times.get)
        if target_file != last_file_loaded:
            # Get the absolute path of the last modified file
            target_file_path = Path(target_file).absolute()
            # Trigger the etl pipeline
            pipeline_data(target_file_path)
            last_file_loaded = target_file
        time.sleep(DIRECTORY_WATCH_SLEEP)


def pipeline_data(filepath: Path):
    """
    Our extract-transform-load process(ETL)

    :param filepath: A network-file-system(nfs) path containing data created from CatWatcher
    """
    pipeline_run_id = uuid.uuid4()
    LOGGER.info(f"Starting ETL pipeline {pipeline_run_id} for file {filepath}")

    try:
        extract_cat_data(filepath, pipeline_run_id)  # Place holder
        cat_data = transform_cat_data(filepath, pipeline_run_id)
        load_cat_data(cat_data, pipeline_run_id)
    except sqlalchemy.exc.IntegrityError as e:
        LOGGER.error(f"ETL pipeline {pipeline_run_id} Encountered IntegrityError {e}")
        if "duplicate key value violates unique constraint" in str(e):
            LOGGER.info(
                f"ETL pipeline {pipeline_run_id} Duplicate key detected, removing file {filepath}"
            )
            filepath.unlink(True)
    except Exception as e:
        LOGGER.error(
            f"ETL pipeline {pipeline_run_id} encountered an error, aborting - {e}"
        )
        return
    # if clean_on_success:
    #    LOGGER.info(f"ETL pipeline {pipeline_run_id} removing file {filepath}")
    #    filepath.unlink(True)
    LOGGER.info(f"ETL pipeline {pipeline_run_id} complete")


def extract_cat_data(filepath: Path, pipeline_run_id: uuid.UUID) -> Path:
    """
    pass for now.
    """
    LOGGER.info(
        f"ETL pipeline {pipeline_run_id} - Extracting contents of file {filepath}"
    )
    return filepath


def transform_cat_data(filepath: Path, pipeline_run_id: uuid.UUID) -> list:
    """
    Extract the target csv data
    Convert the data in each column into matching datatypes defined in models.py

    :Param filepath: the path of the target file
    Returns a list of CatData objects (only one row atm 20230223)
    """
    LOGGER.info(f"ETL pipeline {pipeline_run_id} - Transforming csv data into CatData.")
    with open(filepath, encoding="utf-8") as csv_file:
        # DictReader returns each row as an ordered dictionary with key names from the header row.
        # https://www.andrewvillazon.com/move-data-to-db-with-sqlalchemy/
        # python3.6 make this row OrderedDict
        cat_data_csv_reader = csv.DictReader(csv_file, quotechar='"')
        cat_data = [_from_orderedDict(row) for row in cat_data_csv_reader]
    return cat_data


def _from_orderedDict(row: OrderedDict) -> CatData:
    """
    Change data type to the ones that are defined in the models.py.
    
    :Param row: OrderedDict of a row from the csv data
    Returns a CatData object
    """
    # Change OrderedDict to dict. Actually we shouldn't need it because we are using python 3.10
    #row = dict(row)
    # Entry and Depart in the raw data need to be converted to datetime type
    row["entry"] = datetime.fromtimestamp(float(row["entry"]))
    row["depart"] = datetime.fromtimestamp(float(row["depart"]))
    return CatData(**row)


def load_cat_data(
    cat_data: List[CatData],
    pipeline_run_id: uuid.UUID
):
    """
    Load cat_data into database at DATABASE_URL

    :Param cat_data: a list of CatData objects (CatData class is defined in models.py)
    """
    LOGGER.info(f"ETL pipeline {pipeline_run_id} - Loading CatData to database...")
    LOGGER.info(f"ETL pipeline {pipeline_run_id} - Beginning database session...")

    # 20220920 debug
    LOGGER.info(f"DATABASE_URL used is {DATABASE_URL}")

    cat_schema_engine = create_engine(DATABASE_URL)
    # Create the cat_data_schema table in the database based on the model defined in models.py if not existed
    _create_schema_if_not_exist(cat_schema_engine, SCHEMA_NAME)
    # Create the cat_data table in the database based on the model defined in models.py if not existed
    Base.metadata.create_all(bind=cat_schema_engine, checkfirst=True)

    # sessionmaker acts as a factory for Session objects
    Session = sessionmaker(bind=cat_schema_engine)
    # Then create individual sessions off the global Session
    with Session() as s:
        # Add the object to the session and commit
        s.add_all(cat_data)
        s.commit()
    
    # Close the engine
    cat_schema_engine.dispose()

    LOGGER.info(f"ETL pipeline {pipeline_run_id} - Loading cat_data complete")


def _create_schema_if_not_exist(engine, schema_name):
    # create schema if it doesn't exist
    from sqlalchemy.schema import CreateSchema
    with engine.connect() as conn:
        if not conn.dialect.has_schema(conn, schema_name):
            conn.execute(CreateSchema(schema_name))
            LOGGER.info(f"The schema {schema_name} created successfully!")

# watch_dir = "/home/emma_dev22/CatWatcher/output/"  # to modify
# file_watcher(watch_dir)
