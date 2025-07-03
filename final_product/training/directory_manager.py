import json
import os
from file_manager import FileManager
from typing import Union,Optional


class DirectoryManager:
    def __init__(self,dir_path:str):
        self.dir_path = dir_path