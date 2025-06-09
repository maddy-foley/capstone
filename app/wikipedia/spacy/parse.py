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




def read_files_by_dir(directory):
    res = []
    for file in os.listdir(directory):
        fp = os.path.join(directory,file)
        file_name = file[:-5]
        file_sem = nlp(file_name)
        dic = {}
        # dic[file_name] = set()
        with open(fp,'r') as html:
            soup = BeautifulSoup(html, 'html.parser')
            # if "may refer to" in soup.text.lower():
            #     print(file_name)
                
            if soup.li:
                text = soup.li.text.strip() + soup.ul.text.strip()
                
                doc = nlp(text)
                # build_word_list= set()
                build_word_list = []
                # for chunk in doc.noun_chunks:
                for token in doc:
                    if token.pos_ == "NOUN":
                        print(token.text,[child for child in token.children])
                    # if file_sem.similarity(token) >= .7:
                    #     print(token.text)
                    #     # build_word_list.add(token.text.lower())
                    # if file_name in token.text:
                    #     break
                # dic[file_name] = build_word_list
    #     dic[file_name] += build_word_list
    # return res


for c in categories:
    directory = f"app/wikipedia/html/{c}"
    res = read_files_by_dir(directory)
    # categories[c] += res

# with open("app/wikipedia/parsed/apparel-accessories-fabric.json",'w') as f:
#     f.write(json.dump(res))