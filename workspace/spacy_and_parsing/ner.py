import spacy
from spacy.language import Language


nlp_lg = spacy.load("output/model-last")
# my_model = spacy.load("output/model-best")

doc = nlp_lg("this chain Necklace is a good example.")

for token in doc:
    print(token.ent_type_)

