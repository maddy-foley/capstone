import json
import spacy
from custom_common.file_manager import CustomHTMLFile,CustomJSONFile
from bs4 import BeautifulSoup
import re


nlp = spacy.load("en_core_web_sm")
data_dic = {}

my_dir = CustomHTMLFile('data/raw-html/google')
text_dirs = my_dir.get_all_file_paths()

def get_file_text(file_path):
    with open(file_path) as file:
        soup = BeautifulSoup(file,'html.parser')

        my_text = ' '.join(soup.getText(separator=' ').strip().split())
        return my_text
    
def get_lemmas(word_phrase: str):
    key_word_doc = nlp(word_phrase)
    word_lemmas =[w.lemma_ for w in key_word_doc]
    return word_lemmas




def analyze_texts(text_dirs):
    product_sents = []
    ellip = []
    store_sents = []
    other = []
    visited = []
    i = 0

    for t in text_dirs:
        dic = {}
        doc = nlp(get_file_text(t))
        path_arr = t.split('/')
        word = path_arr.pop()[:-8].replace('_',' ')
        category = path_arr.pop()
        if category not in data_dic:
            data_dic[category] = []
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
                            # product_sents.append(token.sent.text)
                    visited.append(token.sent.text)
        i += 1
        data_dic[category].append({word:all_sentences})
        print('category: ', category,i)

    
temp = analyze_texts(text_dirs)

for d in data_dic:
    # for i,key in enumerate(data_dic[d]):
    'writing'
    for key in data_dic:
        print('writting: key \n')
        my_json = CustomJSONFile(f"data/parsed/parsed_google/{key}")
        my_json.write_new_json_file(data_dic[key])