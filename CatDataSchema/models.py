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


    

