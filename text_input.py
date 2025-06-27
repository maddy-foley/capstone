from bs4 import BeautifulSoup
import spacy 


def get_text_from_html_file_path(file_path: str):
    soup = BeautifulSoup(file_path,'html.parser')
    parsed_html = soup.text
    return parsed_html
