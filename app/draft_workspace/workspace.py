from data_parsing.custom_common.file_manager import CustomJSONFile
import spacy

nlp = spacy.load('en_core_web_trf')

doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)
