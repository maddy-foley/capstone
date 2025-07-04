from file_manager import FileManager,JSONFileManager
import spacy
# Data from training session
all_training_data = {
}
my_nlp = spacy.load('output_fin/model-best')

file = FileManager("notebook/pipe_line_output.txt")
content = file.read_file()

names = ['E', '#', 'TOK2VEC_LOSS', 'NER_LOSS', 'ENTS_F', 'ENTS_P', 'ENTS_R', 'SCORE']
all_training_data = {n:[] for n in names}
for line in content[2:]:
    parsed_line = [x for x in line.split(' ') if x != '']
    for i in range(len(names)):
        all_training_data[names[i]].append(parsed_line[i])



over_all_stats = all_training_data.keys()


best_performance = {}

performance_met = my_nlp.meta['performance']
for key in performance_met:
    item = performance_met[key]
    if key.upper() in over_all_stats:
        best_performance[key.upper()] = item

res = {'best': best_performance ,'all': all_training_data}

json_file = JSONFileManager("notebook")
json_file.write_json_file(res,'all_pipeline_stats')