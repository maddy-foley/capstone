import json
import os
from bs4 import BeautifulSoup


class FileManager:
    def __init__(self,file_path:str):
        self.file_path = file_path
        self.dir_arr = file_path.split('/')
        self.type = ''
        self.get_file_type()
        
    def get_file_type(self):
        file_name = self.dir_arr[-1].split('.')
        self.type = file_name[-1]

    def read_file(self):
        try:
            with open(self.file_path,'r') as file:
                text = ''
                if self.type == 'json':
                    text = self.read_json(file)
                elif self.type == 'html':
                    text = self.read_html(file)
                else:
                    text = file.read()
                file.close()
                
                return text
                
        except FileNotFoundError:
            print(f"Error: The file {self.file_path} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def read_json(self,file):
        return json.load(file)

    def read_html(self,file):
        soup = BeautifulSoup(file,'html.parser')
        return '. '.join([str(text) for text in soup.stripped_strings])