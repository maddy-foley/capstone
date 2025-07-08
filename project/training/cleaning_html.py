import json
import spacy
from project.file_manager import JSONFileManager
from project.directory_manager import DirectoryManager
from bs4 import BeautifulSoup
import re


nlp = spacy.load("en_core_web_lg")
data = {}

directory = DirectoryManager('final_product/training/unclean_data/google_html')
file_paths = directory.get_all_dir_file_names(sub_dir=True)

def get_file_text(file_path):
    with open(file_path) as file:
        soup = BeautifulSoup(file,'html.parser')

        my_text = ' '.join(soup.getText(separator=' ').strip().split())
        return my_text
    
def get_lemmas(word_phrase: str):
    key_word_doc = nlp(word_phrase)
    word_lemmas =[w.lemma_ for w in key_word_doc]
    return word_lemmas




def analyze_texts(file_paths):
    ellip = []
    store_sents = []
    visited = []
    i = 0
    
    for t in file_paths:
        print("opening file: ", t)
        doc = nlp(get_file_text(t))
        path_arr = t.split('/')
        word = path_arr.pop()[:-8].replace('_',' ')
        all_sentences = []
        word_lemmas = get_lemmas(word)

        for token in doc:
            if token.sent.text in visited:
                continue
            if token.lemma_.lower() in word_lemmas:
                if token.sent.text[-1] == '.':
                    if 'store rating' in token.sent.text.lower():
                        store_sents.append(token.sent.text)
                    elif '...' in token.sent.text.lower():
                        ellip.append(token.sent.text)
                    else:
                        no_url = True
                        for item in token.sent:
                            if item.like_url:
                                no_url = False
                        if no_url:
                            all_sentences.append(token.sent.text)
                    visited.append(token.sent.text)
       
        i += 1
        data[word]= all_sentences


    
temp = analyze_texts(file_paths)

for d in data:
    print(f"writing: {d}")
    my_json = JSONFileManager(f"final_product/training/clean_data/product_json/")
    my_json.write_json_file({d:data[d]},d)