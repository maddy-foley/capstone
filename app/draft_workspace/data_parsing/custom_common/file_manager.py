import json
import os
import re
from typing import Union, Optional
import sys
from bs4 import BeautifulSoup
import collections

# NEED TO FIX, built quickly to make parsing faster

class CustomFile:
    def __init__(self,directory,file_type_suffix:str):
        self.directory = directory
        self.file_type_suffix = file_type_suffix

    # get next available version number to name file
    def get_next_version_count(self,dir=None):
        version_num = 1
        while os.path.exists(self.get_formatted_version_string(version_num)):
            version_num += 1
            
        return self.get_formatted_version_string(version_num)

    def format_version_count(self,count):
        return str(count).zfill(2)
    
    def get_formatted_version_string(self,version_num: int):
        return f"{self.directory}_{self.format_version_count(version_num)}{self.file_type_suffix}"

    def get_all_sub_directories(self):
        arr = []
        for dir in os.listdir(self.directory):
            arr.append(dir)
        return arr
    
    # note if you want to find all in immediate subdirectories
    def get_all_file_paths(self,sub=False):

        if sub:
            dir = [f"{self.directory}/{s}/"  for s in self.get_all_sub_directories()]
            for path in os.listdir(self.directory):
                for file in os.listdir(path):
                    all_dir.append(path+file)
            return all_dir
        else:
            dir = self.directory
        all_dir = []
        for path in os.listdir(self.directory):
            all_dir.append(f"{self.directory}/{path}")
        return all_dir

    def get_all_version_paths_of_file(self,name):
        arr = []
        for file in os.listdir(self.directory):
            if name in file:
                arr.append(file)
        return arr

    
class CustomJSONFile(CustomFile):
    def __init__(self,directory,file_type_suffix='.json'):
        super().__init__(directory,file_type_suffix)

    def write_new_json_file(self,input:Union[dict,list]):
        save_path = None
        try:
            save_path = self.get_next_version_count()

            with open(save_path,'w') as file:
                file.writelines(json.dumps(input))
                file.close()
                print(f"Saved file as {save_path}")

        except ValueError:
            print("Invalid Input")
            print("Input Type = ", type(input))
            if os.path.exists(save_path):
                os.remove(save_path)
                print("Deleted empty file")
        except Exception as e:
        # Code to handle other exceptions
            print(f"An error occurred: {e}")
            if os.path.exists(save_path):
                os.remove(save_path)
                print("Deleted empty file")
       
    def write_update_to_json_file_dir(self,input: Union[dict,list]) -> None:
        save_path = None
        try:
            save_path = self.get_next_version_count()

            with open(save_path,'w') as file:
                file.writelines(json.dumps(input))
                file.close()
                print(f"Saved file as {save_path}")

        except ValueError:
            print("Invalid Input")
            print("Input Type = ", type(input))
            if os.path.exists(save_path):
                os.remove(save_path)
                print("Deleted empty file")
        except Exception as e:
        # Code to handle other exceptions
            print(f"An error occurred: {e}")
            if os.path.exists(save_path):
                os.remove(save_path)
                print("Deleted empty file")

    # get all override to handle json
    def get_content_from_version_num(self,num):
        file_path = self.get_formatted_version_string(num)
        with open(file_path) as file:
            return json.load(file)

    def get_content_from_file_path(self,file_path:str):
        with open(file_path) as file:
            return json.load(file)

class CustomHTMLFile(CustomFile):
    def __init__(self,directory,file_type_suffix='.html'):
        super().__init__(directory,file_type_suffix)

    def get_text_from_raw_html(self,file_path:Optional[str],target_tag: Optional[str]):

        with open(file_path) as file:
            soup = BeautifulSoup(file,'html.parser')
            if target_tag:
                current_text_selection = soup.find_all(target_tag)
                return list(current_text_selection)
            else:
                current_text_selection = soup.text
            return current_text_selection
    


    def write_to_html_file_dir(self,input: str) -> None:
        try:
            save_path = self.get_next_version_count()

            with open(save_path,'w') as file:
                file.write(BeautifulSoup(input).prettify())
                file.close()
                print(f"Saved file as {save_path}")

        except ValueError:
            print("Invalid Input")
            print("Input Type = ", type(input))
            if os.path.exists(save_path):
                os.remove(save_path)
                print("Deleted empty file")
        except Exception as e:
        # Code to handle other exceptions
            print(f"An error occurred: {e}")
            if os.path.exists(save_path):
                os.remove(save_path)
                print("Deleted empty file")

    def prettify_all_html_versions(self,name):
        paths = self.get_all_version_paths_of_file(name)

        for p in paths:
            file_path = f"{self.directory}/{p}"
            formatted_html = ""
            with open(file_path,'r') as html_file:
                soup = BeautifulSoup(html_file)
                formatted_html = soup.prettify()
                html_file.close()
            with open(file_path,'w') as html_file:
                html_file.write(formatted_html)
                html_file.close()

__all__ = ["CustomFile","CustomJSONFile","CustomHTMLFile"]