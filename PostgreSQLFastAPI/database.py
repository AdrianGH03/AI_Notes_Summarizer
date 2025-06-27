from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# Load environment variables from a .env file into the environment
load_dotenv()

# Get the database URL from the environment variable (set in .env)
URL_DATABASE = os.getenv('DATABASE_URL')

# Create a SQLAlchemy engine instance using the database URL
engine = create_engine(URL_DATABASE)

# Set up a session factory for creating new database sessions
# autocommit=False: changes are not committed automatically
# autoflush=False: changes are not flushed to the database automatically
# bind=engine: sessions will use the engine created above
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models (used for defining tables)
Base = declarative_base()