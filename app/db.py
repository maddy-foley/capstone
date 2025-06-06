from sqlalchemy import create_engine
from models import BaseModel
import os

# load_dotenv()


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
DB_URL = f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"



#build sqlalchemy engine

engine = create_engine(f"postgresql+psycopg2://{DB_URL}",echo=True)
# logging.basicConfig()
# logging.getLogger("sqlalchemy.dialects.postgresql").setLevel(logging.INFO)
BaseModel.metadata.create_all(engine)
