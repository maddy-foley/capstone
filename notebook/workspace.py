from file_manager import FileManager
import spacy

nlp = spacy.load('en_web_core_lg')
html_file = FileManager('./workspace_draft/data/raw-html/google/children_or_infant_wear/bib_01.html')
file_content = html_file.read_file(test=True)

for sent in file_content:
    doc = nlp(sent)
    