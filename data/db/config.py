from sqlalchemy import create_engine, create_mock_engine
from sqlalchemy.orm import Session
from models import BaseModel,Category,Site,SearchQuery
from dotenv import load_dotenv
import psycopg2
import logging
import os
from sqlalchemy import MetaData

# load_dotenv()


# # google search api base url configuration
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
DB_URL = f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"



#build sqlalchemy engine

engine = create_engine(f"postgresql+psycopg2://{DB_URL}",echo=True)
logging.basicConfig()
logging.getLogger("sqlalchemy.dialects.postgresql").setLevel(logging.INFO)
BaseModel.metadata.create_all(engine)




# print(BaseModel.metadata.tables)
