"""Some initialization settings for the sqlalchemy.orm framework."""
import os
import locale
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


def get_engine():
    """Set the database engine according to the system environment."""
    # Check the environment variables for the existence of tests and docstring
    testing = os.getenv("CYBERMARKET")
    if testing == "TESTING":
        engine = create_engine('sqlite:///:memory:', echo=False)
    elif testing == "DOCSTRING":
        engine = create_engine('sqlite:///:memory:', echo=False)
    else:
        # If it does not exist, use the default database
        engine = create_engine(
            'sqlite:///./database/cybermarket.db',
            echo=False
            )
    return engine


# Language setting
lang = locale.setlocale(locale.LC_ALL, ("en_US", "UTF-8"))

# Establish database connection
engine = get_engine()

# Define the base class that maps database tables and python classes
Base = declarative_base()

# Create database session
Session = sessionmaker(bind=engine)

# The custom class can be used to construct a new Session
session = Session()
