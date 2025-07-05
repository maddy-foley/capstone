from file_manager import FileManager,JSONFileManager

# Data from training session
all_training_data = {
}


file = FileManager("notebook/pipe_line_output.txt")
content = file.read_file()

names = ['E', '#', 'LOSS TOK2VEC', 'LOSS NER', 'ENTS_F', 'ENTS_P', 'ENTS_R', 'SCORE']
all_training_data = {n:[] for n in names}
for line in content[2:]:
    parsed_line = [x for x in line.split(' ') if x != '']
    for i in range(len(names)):
        all_training_data[names[i]].append(parsed_line[i])

json_file = JSONFileManager("notebook")
json_file.write_json_file(all_training_data,'pipeline_stats')