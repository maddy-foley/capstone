from config import engine
from models import *
from sqlalchemy.orm import Session

with Session(engine) as session:
    
