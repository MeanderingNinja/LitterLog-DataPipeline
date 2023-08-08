from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    Date,
)

TABLE_NAME = "cat_litterbox_time_data"
SCHEMA_NAME = "cat_data_schema"
Base = declarative_base()


class CatData(Base):
    """
    Represents a table for storing cat litterbox time data.

    Attributes:
        __tablename__ (str): The name of the table.
        __table_args__ (dict): Additional arguments for the table, such as the schema.
        id (Column): Primary key column for the table.
        date (Column): Column for storing the date of the litterbox activity.
        entry (Column): Column for storing the entry time of the cat.
        depart (Column): Column for storing the departure time of the cat.
        duration (Column): Column for storing the duration of the litterbox activity.
    """

    __tablename__ = TABLE_NAME
    __table_args__ = {"schema": SCHEMA_NAME}
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    entry = Column(DateTime)
    depart = Column(DateTime)
    duration = Column(Float)

    ####### @validates may need to be added later on ##############
