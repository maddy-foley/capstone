import json
import os
from bs4 import BeautifulSoup
from typing import Union,Optional

# this was just to help repetative tasks like opening and saving files

class FileManager:
    def __init__(self,file_path:str):
        self.file_path = file_path
        self.dir_arr = file_path.split('/')
        self.type = ''
        self.get_file_type()
        
    def get_file_type(self):
        file_name = self.dir_arr[-1].split('.')
        self.type = file_name[-1]

    def get_file_name(self):
        file = self.dir_arr[-1]
        return file[:file.find('_0')]

    def read_file(self,test=False):
        try:
            with open(self.file_path,'r') as file:
                text = ''
                if self.type == 'json':
                    text = self.read_json(file)
                elif self.type == 'html':
                    if test:
                        text = self.test_methods(file)
                    else:
                        text = self.read_html(file)
                else:
                    text = [x.strip() for x in file.readlines()]
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
    
    
class HTMLFileManager(FileManager):
    def __init__(self,file_path):
        super().__init__(file_path)

    def parse_html(self,file_path:Optional[str]):
        with open(file_path,'r') as file:
            soup = BeautifulSoup(file,'html.parser')
            soup_arr = [str(text) for text in soup.stripped_strings if text.count(' ') > 0]
            
            return soup_arr
        
class JSONFileManager(FileManager):
    def __init__(self,file_path):
        super().__init__(file_path)

    def write_json_file(self,input:Union[dict,list],name=None):
        if name:
            save_path = f"{self.file_path}/{name}.json"

        with open(save_path,'w') as file:
            file.writelines(json.dumps(input))
            file.close()
            print(f"Saved file as {save_path}")