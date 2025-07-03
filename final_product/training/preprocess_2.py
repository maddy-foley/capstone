import spacy
from spacy.tokens import DocBin,Doc
from file_manager import FileManager
import re
import time
from spacy.training import Example



nlp_en = spacy.blank('en')
nlp = spacy.load("en_core_web_lg")


all_html_paths = []