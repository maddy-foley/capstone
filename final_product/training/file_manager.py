import json
import os
from bs4 import BeautifulSoup
from typing import Union,Optional


class FileManager:
    def __init__(self,file_path:str,file_suffix=None):
        self.file_path = file_path
        self.dir_arr = file_path.split('/')
        self.file_suffix = file_suffix
        if file_suffix == None:
            self.get_file_type()
        
    def get_file_type(self):
        file_name = self.dir_arr[-1].split('.')
        self.file_suffix = file_name[-1]

    def get_file_name(self):
        file = self.dir_arr[-1]
        return file[:file.find('_0')]

    def read_file(self,test=False):
        try:
            with open(self.file_path,'r') as file:
                text = ''
                if self.file_suffix == 'json':
                    text = self.read_json(file)
                elif self.file_suffix == 'html':
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
    
    def get_next_version_count(self,name):
        version_num = 1
        while os.path.exists(self.get_formatted_version_string(version_num,name)):
            version_num += 1
            
        return self.get_formatted_version_string(version_num,name)

    def format_version_count(self,count):
        return str(count).zfill(2)

    def get_formatted_version_string(self,version_num,name):
        name = name.replace(' ','_')
        if self.file_path[-1] == '/':
            return f"{self.file_path}{name}_{self.format_version_count(version_num)}{self.file_suffix}"
        else:
            return f"{self.file_path}/{name}_{self.format_version_count(version_num)}{self.file_suffix}"
    
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
        super().__init__(file_path,file_suffix='.json')

    def write_json_file(self,input:Union[dict,list],name:str):

        save_path = self.get_next_version_count(name)

        with open(save_path,'w') as file:
            file.writelines(json.dumps(input))
            file.close()
            print(f"Saved file as {save_path}")

