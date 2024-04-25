"""Some initialization settings for the sqlalchemy.orm framework."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Establish database connection
engine = create_engine('sqlite:///database/cybermarket.db', echo=False)

# Define the base class that maps database tables and python classes
Base = declarative_base()

# Create database session
Session = sessionmaker(bind=engine)

# The custom class can be used to construct a new Session
session = Session()
