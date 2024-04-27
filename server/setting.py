"""Some initialization settings for the sqlalchemy.orm framework."""
import locale
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Language setting
lang = locale.setlocale(locale.LC_ALL, ("en_US", "UTF-8"))

# Establish database connection
engine = create_engine('sqlite:///database/cybermarket.db', echo=False)

# Define the base class that maps database tables and python classes
Base = declarative_base()

# Create database session
Session = sessionmaker(bind=engine)

# The custom class can be used to construct a new Session
session = Session()
