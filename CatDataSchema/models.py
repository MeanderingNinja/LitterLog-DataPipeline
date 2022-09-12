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

Base = declarative_base()

# Create CatData class with table name cat_data. This is the table name that will show up in Postges.
class CatData(Base):
    __tablename__ = "cat_data"
    # __table__args__ = {"schema":"cat_tech_database"}  I saw this line here: https://www.youtube.com/watch?v=oNky1SUC5Ak
    id = Column(Integer, primary_key=True)
    date = Column(Date)  # May change the column name to Date in the csv later
    entry = Column(DateTime)
    depart = Column(DateTime)
    duration = Column(Float)

    ####### @validates may need to be added later on ##############

    

