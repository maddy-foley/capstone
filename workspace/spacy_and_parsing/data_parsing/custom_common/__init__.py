# import json
# import os
# import re
# from typing import Union, Optional
# import sys

# class CustomFile:
#     def __init__(self,directory_name: str, name: Optional[str],count=0,file_type_suffix=Optional[str]):
#         self.dir = directory_name
#         self.name = name
#         self.next_version_count = count
#         self.file_type_suffix = file_type_suffix

#         self.set_next_version_count()

#     def format_count(self,count=None):
#         if count:
#             return count.zfill(2)
#         else:
#             return self.next_version_count.zfill(2)    

#     def set_next_version_count(self) -> int:
#         version_num = 0
#         while os.path.exists(f"{self.dir}/{self.name}_{self.format_count(version_num)}{self.file_type_suffix}"):
#             version_num += 1

#         self.next_version_count = version_num

#     # get full file path to save input to
#     def get_new_save_file_path(self) -> str:
#         file_path = f"{self.dir}/{self.name}_{self.format_count()}{self.file_type_suffix}"
#         return file_path