from directory_manager import DirectoryManager
from file_manager import FileManager
import spacy
from spacy.tokens import DocBin,Doc
from bs4 import BeautifulSoup


nlp = spacy.load("en_core_web_sm")


directory = DirectoryManager('project/training/unclean_data/google_html')
file_paths = directory.get_all_dir_file_names(sub_dir=True)

def get_file_text(file_path):
    name = file_path.split('/').pop()[:-8]
    with open(file_path, encoding='utf-8') as file:
        soup = BeautifulSoup(file,'html.parser')

        my_text = ' '.join(soup.getText(separator=' ').strip().split())
        
        
        return my_text, name
   
visited = []

def annotate_ent(file_path):
    train_data = []
    dev_data = []
    total = 0
    text, name = get_file_text(file_path)
    name_doc = nlp(name.replace("_"," "))
    key_lemma = " ".join([x.lemma_ for x in name_doc])
    hyphen = False
    if '-' in key_lemma:
        hyphen = True
    key_len = len(name_doc)
    doc = nlp(text)
    print(f"processing: {key_lemma}")
    for sent in doc.sents:
        if sent.text in visited:
            continue
        visited.append(sent.text)
        sent_doc = nlp(sent.text)
        ents = ['O'] * len(sent_doc)
        tokens_found = 0
        # spans = ['O'] * len(sent)
        for i in range(len(sent)-key_len):
            span = sent_doc[i:i+key_len]
            
            if span.lemma_.lower() == key_lemma:
                for j in range(key_len):
                    if j == 0:
                        ents[i] = 'B-PRODUCT'
                    else:
                        ents[i + j] = 'I-PRODUCT'

        # for token in sent_doc:
        #     if token.i + key_len >= len(sent_doc):
        #         if tokens_found > 0 and tokens_found <= key_len and spans[-1] != 'O' :
        #             spans.append('I-PRODUCT')
        #             tokens_found += 1
        #         else:
        #             spans.append('O')
        #             tokens_found = 0
        #     else:
        #         lemmas = [l.lemma_.lower() for l in sent_doc[token.i:token.i+key_len]]
        #         lemma = ' '.join(lemmas)
        #         # print(lemma,key_lemma)
        #         if key_lemma == lemma:
        #             spans.append('B-PRODUCT')
        #             tokens_found = 1
        #         # catch if key is plural incase lemmatizer has issues
        #         elif key_lemma + 's' == lemma:
        #             spans.append('B-PRODUCT')
        #             tokens_found  = 1
        #         elif spans != [] and spans[-1] != 'O':
        #             spans.append('I-PRODUCT')
        #             tokens_found += 1
        #         else:
        #             spans.append('O')
        #             tokens_found = 0
        if ents != [] and 'B-PRODUCT' in ents:
            total += 1
            if total % 9 == 2:
                dev_data.append((sent_doc,{"entities": ents}))
            else:
                train_data.append((sent_doc,{"entities": ents}))

 
            
                
    return train_data, dev_data


def find_and_save_all_ents(file_paths):
    db_train = DocBin()
    db_dev = DocBin()
    for file_path in file_paths:
        if ".DS_Store" in file_path:
            continue
        train_data,dev_data = annotate_ent(file_path)

        for item in train_data:
            doc = item[0]
            ents = item[1]['entities']
            words = []
            spaces = []
            for i, token in enumerate(doc):
                words.append(token.text)
                has_ws = token.whitespace_ == ' '
                spaces.append(has_ws)

        
            new_doc = Doc(nlp.vocab,words=words,ents=ents,spaces=spaces)
            db_train.add(new_doc) 

        for item in dev_data:
            doc = item[0]
            ents = item[1]['entities']
            words = []
            spaces = []
            for i, token in enumerate(doc):
                words.append(token.text)
                has_ws = token.whitespace_ == ' '
                spaces.append(has_ws)

        
            new_doc = Doc(nlp.vocab,words=words,ents=ents,spaces=spaces)
            db_dev.add(new_doc) 


    db_train.to_disk("./train.spacy")
    db_dev.to_disk("./dev.spacy")

find_and_save_all_ents(file_paths)