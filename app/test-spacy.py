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
open = []

def get_site_snippet_pos_by_id(id):
    with Session(engine) as session:
        stmt = select(Site).where(Site.id== id)
        site = session.scalars(stmt).one()
        nlp = spacy.load("en_core_web_sm")

        """ # uncommit to change parser to senter makes parsing faster """
        # nlp.disable_pipe("parser")
        # nlp.enable_pipe("senter")

        doc = nlp(site.snippet.lower())
        adj = []
        noun = []
        # return doc
        for token in doc:
            print(token.text,token.tag_)
            # print(token.lemma_, token.pos_, token.tag_)
            if token.pos_ == 'ADJ':
                adj.append(token.text)
            if token.pos_ == 'NOUN':
                noun.append(token.text)
        
        print("adj: " , adj)
        print("noun: " , noun)
    

# def get_site_snippet_adj_by_id(id):
    
#     doc = get_site_snippet_pos_by_id(id=id)
#     for token in doc:
#         print(doc.pos_)

# get_site_snippet_adj_by_id(3)
get_site_snippet_pos_by_id(42)

"""
Training:
https://spacy.io/usage/training#training-data
- look at data utilities section
examples:
https://github.com/explosion/projects/tree/v3/tutorials

Converter:
https://spacy.io/api/cli#convert


"""