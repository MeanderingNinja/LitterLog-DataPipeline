"""
1. Tested that using session to commit a row of data to 
a database that hasn't yet have a table created in it produces error:
"sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedTable) relation "books" does not exist" 
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()
# We need to inherit Base in order to register models with SQA. 
# Without this, SQA wouldn't know anything about our models.
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    pages = Column(Integer)
    published = Column(Date)

from sqlalchemy import create_engine
# Engine give SQLAlchemy the power to create tables 
DATABASE_URL = "postgresql+psycopg2://metabase_catwatcher_user:metabase_catwatcher_pw@192.168.1.157:5432/metabase_catwatcher_db"
engine = create_engine(DATABASE_URL)

from sqlalchemy.orm import sessionmaker
# sessionmaker acts as a factory for Session objects
Session = sessionmaker(bind=engine)
# Then create individual sessions off the global Session
s = Session()
# Make a instance of the model class cat_data with one row of data, e.g. 
from datetime import datetime
row = Book(id=1, title="The Good Book", author="Emma Li", pages=180, published=datetime.today())
# Add the object to the session and commit
s.add(row)
print("Good right after add and before commit")
s.commit()
print("Good right after commit")

# Now the data should be in the table created from models.py

# Always close the session when you are done
s.close()
