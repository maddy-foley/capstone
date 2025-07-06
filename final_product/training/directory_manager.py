import json
import os
from file_manager import FileManager
from typing import Union,Optional


class DirectoryManager:
    def __init__(self,directory:str):
        self.directory = directory
    
    def get_all_imediate_subdirectories(self):
        arr = []
        for dir in os.listdir(self.directory):
            arr.append(self.directory + '/' + dir)
        return arr
    
    def get_all_dir_file_names(self,sub_dir=False):
        all_file_names = []
        if sub_dir:
            dirs = self.get_all_imediate_subdirectories()
            # print(dirs)
            for path in dirs:
                for file in os.listdir(path):
                    all_file_names.append(f"{path}/{file}")
            return all_file_names
        else:
            all_file_names = []
            for path in os.listdir(self.directory):
                all_file_names.append(f"{self.directory}/{path}")

            return all_file_names