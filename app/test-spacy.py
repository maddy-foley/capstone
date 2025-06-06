import spacy
import en_core_web_sm
from sqlalchemy.orm import Session
from sqlalchemy import select,join
import os
from sqlalchemy import create_engine
from models import Site,SearchQuery,Category
import os


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
DB_URL = f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"

engine = create_engine(f"postgresql+psycopg2://{DB_URL}",echo=True)

# nlp = spacy.load("en_core_web_sm")
# nlp = en_core_web_sm.load()
# tokens = nlp("dog cat banana afskfsd")

# for token in tokens:
#     print(token.text, token.has_vector, token.vector_norm, token.is_oov)


def get_lemmas(id):
    with Session(engine) as session:
        stmt = select(Site).where(Site.id== id)
        site = session.scalars(stmt).one()
        print(site.snippet)
    # nlp = spacy.load("en_core_web_sm")
    # doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
    # with Session(engine) as session:
    #     # stmt = select(Site).where(id=id)
    #     print(stmt)

    # for token in doc:
    #     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
    #             token.shape_, token.is_alpha, token.is_stop)
    

get_lemmas(1)
