import spacy
import en_core_web_sm
import os
from bs4 import BeautifulSoup
import sys
import re
import json

nlp = spacy.load("en_core_web_sm")

categories = {"accessories":[],"apparel":[],"fabric": []}

""" 
Important Spacy Method Notes:


DOC:
- doc.noun_chunks useful for finding NP


TOKEN:
- token.dep_ similar to phrase structure rules
- token.pos_ provides general POS
- token.tag_ provides additional POS information ( ex: verb is a gerund - look up key )

"""

def read_files_by_dir(base_directory,tag=None):
    res_soups_text = []
    for c in categories:
        directory = base_directory + c
        for file in os.listdir(directory):
            fp = os.path.join(directory,file)
            file_name = file[:-5]
            file_sem = nlp(file_name)
            with open(fp,'r') as html:
                soup = BeautifulSoup(html, 'html.parser')
                if not tag:
                    res_soups_text.append(soup.text)
                elif not soup(tag):   
                    continue
                else:
                    res_soups_text.append([item.text for item in soup.find_all(tag)])

    return res_soups_text

def chunk_nouns(doc_text):
    doc = nlp(doc_text)
    for chunk in doc.noun_chunks:
        print(chunk.text, chunk.root.text, chunk.root.dep_,
                chunk.root.head.text)


soups_text_list = read_files_by_dir("app/wikipedia/html/","li")

print(soups_text_list)