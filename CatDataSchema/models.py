"""
This module defines a declarative base for creating a table in a Postgres database with the table name 'cat_data' and schema name 'cat_data_schema'. 
The table has four columns: 'id', 'date', 'entry', 'depart', and 'duration', which are defined as follows:

id: An Integer column and the primary key of the table
date: A Date column representing the date of the data entry
entry: A DateTime column representing the time when a cat entered a litterbox
depart: A DateTime column representing the time when a cat left a litterbox
duration: A Float column representing the duration of the cat's stay in the litterbox

The CatData class is defined with these columns as attributes, and is used to create an object-relational mapping (ORM) for interacting with 
the cat_data table in the Postgres database. This class inherits from the declarative base provided by the SQLAlchemy package.
"""

# Import the base class our models inherit from
# Without this, SQLAlchemy wouldn't know anything about our models.
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    Date,
)
TABLE_NAME = "cat_data"
SCHEMA_NAME = "cat_data_schema"
Base = declarative_base()

# Create CatData class with table name cat_data. This is the table name that will show up in Postgres.
class CatData(Base):
    __tablename__ = TABLE_NAME
    __table_args__ = {'schema': SCHEMA_NAME}  
    id = Column(Integer, primary_key=True)
    date = Column(Date)  # May change the column name to Date in the csv later
    entry = Column(DateTime)
    depart = Column(DateTime)
    duration = Column(Float)

    ####### @validates may need to be added later on ##############


    

