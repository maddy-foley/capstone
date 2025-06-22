from data_parsing.custom_common.file_manager import CustomJSONFile
import spacy
from spacy.tokens import DocBin
# from app.draft_workspace.spacy.training_model import TraingData

nlp = spacy.load('en_core_web_trf')



# files to access
json_dir = CustomJSONFile('app/data/google_json/google_clean_01')
# my_files = json_dir.get_all_file_paths()


def get_all_content():
    for file_name in my_files:
        # skip lemma file 
        if 'lemma_items' in file_name:
            continue
        content = json_dir.get_content_from_file_path(file_name)
        for obj in content:
            for key in obj:
                for text in obj[key]:
                    doc = nlp(text)
                    print(doc.ents)


# print([c.keys() for c in content])
# for category in content:
#     for word in category:
#         texts = category[word]

# doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

# for token in doc:
#     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#             token.shape_, token.is_alpha, token.is_stop)
my_lemmas = json_dir.get_content_from_file_path('app/data/google_json/google_clean_01/accessories_01.json')

def draft_train(texts):
    db = DocBin()
    for example in texts:
        for key in example:
            
            if len(example[key]) < 3:
                continue
            for text in example[key]:
                training = []
                doc = nlp(text)
                lemma_key = key
                # print(doc.lemmas)
                for token in doc:
                    print(token.i, doc[token.i])
                    # if key == token.lemma_:
                        # print(token.text,token.i, token.i + len(token.text))
                        # span_start = token.i
                        # span_end = token.i + len(token.text)
                        # print(key.sent)
                #     # ents = TraingData(token.sent,token.i,token.idx)
                #     training
                #     continue
            # return example[key]
    pass

json_obj = CustomJSONFile('app/data/google_json/google_clean_01/accessories_01.json')
test_texts = json_obj.get_content_from_file_path('app/data/google_json/google_clean_01/accessories_01.json')
ex = draft_train(test_texts)
