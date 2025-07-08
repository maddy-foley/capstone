from directory_manager import DirectoryManager

directory = DirectoryManager('project/training/unclean_data/google_html')
file_paths = directory.get_all_dir_file_names(sub_dir=True)
names = [] 
def get_file_text(file_path):
    name = file_path.split('/').pop()[:-8]
    name = name.replace('_',' ')
    names.append(name)


for f in file_paths:
    get_file_text(f)

# save_path = "project/data/products.txt"
# with open(save_path,'w') as file:
#         for n in names:
#             file.write(n + "\n")
#         file.close()

print(len(names))