import matplotlib.widgets as wd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from file_manager import JSONFileManager

class DataVisual:
    def __init__(self,file_path):
        self.file_name = file_path
        self.epoch = []
        self.scores = {
            'F-Score':[],
            'Recall': [],
            'Precision':[]
        }
        self.ner_loss = []
        self.best_f = 0.0
        self.get_json(file_path)

    def get_json(self,file_name):
        stats_file = JSONFileManager(file_name)
        stats = stats_file.read_file()
        # ENTS_P = Precision = Formula: True Pos / (True pos + True Neg), high == few false positives
        # ENTS_R = recall = Formula: True Pos / (True pos + True Neg), high == few false negatives
        # ENTS_F = harmony of p and r. This is the MAIN quality score. Formula: F1 = 2 * (P * R) / (P + R)
        # ner_loss = loss from NER component based on how far the predicted entity spans are from the gold annotations.
        # print(stats)
        self.epoch =  [int(x) + 1 for x in stats['mean_epoch']['E']]
        
        self.best_f = stats['best']['ENTS_F']
        ents_f = [float(x) for x in stats['mean_epoch']['ENTS_F']]
        ents_r = [float(x) for x in stats['mean_epoch']['ENTS_R']]
        ents_p = [float(x) for x in stats['mean_epoch']['ENTS_P']]
        self.scores['F-Score'] = ents_f
        self.scores['Recall'] = ents_r
        self.scores['Precision'] = ents_p
        self.ner_loss = [float(x) for x in stats['mean_epoch']['NER_LOSS']]

class BarGraph(DataVisual):
    def __init__(self,file_path):
        super().__init__(file_path)
    
        
    
    def make_graph(self):
        width = 0.25 
        multiplier = 0
        x = np.arange(len(self.epoch))
        fig, ax = plt.subplots(layout='constrained')

        for attribute, measurement in self.scores.items():
            offset = width * multiplier
            rects = ax.bar(x + offset, measurement, width, label=attribute)
            multiplier += 1

        ax.axhline(round(self.best_f,2) * 100, color='purple', linestyle=':', label='Best F-Score')
        ax.set_ylabel('Prediction Score (Percentage)')
        ax.set_xlabel('Epoch')
        ax.set_title('Training Prediction Scores per Epoch')
        ax.set_xticks(x + width, self.epoch)
        ax.legend(loc='upper left', ncols=3)
        ax.set_ylim(60, 100)
        return plt.show()
     
   