from file_manager import FileManager,JSONFileManager
import spacy
from statistics import mean
# Data from training session
all_training_data = {
}
my_nlp = spacy.load('output/model-best')


def write_stats_txt_to_json(file_name):
    file = FileManager(file_name)
    content = file.read_file()
    
    names = ['E', '#', 'TOK2VEC_LOSS', 'NER_LOSS', 'ENTS_F', 'ENTS_P', 'ENTS_R', 'SCORE']
    all_training_data = {n:[] for n in names}
    for line in content[2:]:
        parsed_line = [x for x in line.split(' ') if x != '']
        for i in range(len(names)):
            all_training_data[names[i]].append(float(parsed_line[i]))
    
    mean_epoch_data = {key:[] for key in all_training_data}
    start = 0
    epochs = all_training_data['E']
    
    for i, e in enumerate(epochs):
        if e > epochs[start]:
            for key in mean_epoch_data:
                mean_epoch_data[key].append(round(mean(all_training_data[key][start:i]),2))
            start = i
    
    over_all_stats = all_training_data.keys()
    
    
    best_performance = {}
    last_performance = {}
    
    best_performance_met = my_nlp.meta['performance']
    last_performance_file = JSONFileManager('output/model-last/meta.json')
    last_performance_met = last_performance_file.read_file()['performance']
    
    
    for key in best_performance_met:
        item = best_performance_met[key]
        if key.upper() in over_all_stats:
            best_performance[key.upper()] = item
            last_performance[key.upper()] = last_performance_met[key]
    
    mean_epoch_data['E'] = [x for x in range(len(mean_epoch_data['E']))]        
    
    res = {'best': best_performance ,'all': all_training_data,'mean_epoch':mean_epoch_data,'last':last_performance}
    
    
    json_file = JSONFileManager("project/data")
    json_file.write_json_file(res,'all_pipeline_stats')


# runs a script to load json
write_stats_txt_to_json("pipeline_output.txt")