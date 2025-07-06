import spacy
from spacy import displacy
from file_manager import FileManager
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display
import pandas as pd

class DualDocAnalysis:
    # Initializes both models
    # requires either input text or a file -> Must specify when declairing
    def __init__(self,nlp_model="en_core_web_lg",ner_model="../output_3/model-best",text=None,file=None):
        if file:
            self.text = FileManager(file).read_file()
        else:
            self.text = text
        # Spacy's Pretrained Model
        self.nlp = spacy.load(nlp_model)
        self.nlp_doc = self.nlp(self.text)
        # Custom Product Trained Model
        self.ner = spacy.load(ner_model)
        self.ner_doc = self.ner(self.text)
    
class ProductModel(DualDocAnalysis):
    def __init__(self,text=None,file=None):
        super().__init__(text=text,file=file)
        self.freq = {}
        self.main_entities = []   
        self.ling_info = {}
        self.widget_labels = {
            
            'Adjective(s)': 'ADJ',
            'Noun(s)': 'N',
            'Adverb(s)': 'ADV',
            'Compound Noun(s)':'C_N',
            'Descriptive Neighbors (Misc)': 'DESC_NEIGHBORS'
        }
        self.set_ents()
        self.get_all_doc_ent_ling_info()

    def set_ents(self):
        if len(self.freq) == 0:
            self.freq = {e.text.lower(): 0 for e in self.ner_doc.ents}
            
            for e in self.ner_doc.ents:
                self.freq[e.text.lower()] += 1            
        # analyze entities that appear more than 1 times.
        # project's use case expects the input contains several listings of a single product
        self.main_entities = [e for e in self.ner_doc.ents if self.freq[e.text.lower()] > 1]

    def get_related_spans(self):
    
        span_info = {
            'FULL_NP':[],
            'DESC_NEIGHBORS':[],
            'ADJ':[],
            'ADV':[],
            'N':[],
            'C_N':[]
        }
        
        for key in self.ling_info:
            for span_name in span_info:
                span_info[span_name] += self.ling_info[key][span_name]
        
        return span_info

    def get_all_doc_ent_ling_info(self):
        if self.main_entities == []:
            self.set_ents()

        self.ling_info = {e.text.lower(): {
                'SENT':[],
                'FULL_NP':[],
                'DESC_NEIGHBORS':[],
                'ADJ':[],
                'ADV':[],
                'N':[],
                'C_N':[]
            }
               for e in self.main_entities
        }
        
        for i, ent in enumerate(self.main_entities):
            token = self.nlp_doc[ent.start]
            token_head = token
            lower_token_text = token.text.lower()
            self.ling_info[lower_token_text] = self.get_ling_token_info(token,self.ling_info[lower_token_text])
            
    def get_ling_token_info(self,token,dic):
        # span_dic = {
        #     'FULL_NP':[],
        #     'DESC_NEIGHBORS':[],
        #     'ADJ':[],
        #     'ADV':[],
        #     'N':[],
        #     'C_N':[]
        # }
        if token.sent not in dic.get('SENT'):
        
            dic['SENT'].append(token.sent)

        for t in token.sent:
            lower_token = t.text.lower()
            if t.is_punct or len(t.lemma_) == 1 or t.lemma_ == token.lemma_:
                continue
            elif t.ent_type_ == 'MONEY':
                continue
            elif t.tag_ in ['NN','NNP','VBG']:
                if t.dep_ == 'compound':
                    dic['C_N'].append(t)
                else:
                    dic['N'].append(t)
            elif t.pos_ == 'ADJ':
                dic['ADJ'].append(t)
            elif t.pos_ == 'ADV':
                dic['ADV'].append(t)
            
                
        for chunk in token.sent.noun_chunks:
            if token in chunk:
                dic['FULL_NP'].append(chunk)
                for item in chunk:
                    if item.tag_ in ['NN','NNP','VBG'] and item.text != token.text and (item.text.isalnum() or item.text == '-'):
                        dic['DESC_NEIGHBORS'].append(item)
        return dic

    def get_data_analysis(self):
        
        # self.ling_info = self.get_all_doc_ent_ling_info()
        freq = { e: {
                'TOTAL': len(self.ling_info[e]['SENT']),
                'DESC_NEIGHBORS':{},
                'ADJ':{},
                'ADV':{},
                'N':{},
                'C_N':{}
            }
            for e in self.ling_info
        }
        for ent_key in freq:
            for ling_key in freq[ent_key]:
                if ling_key not in self.ling_info[ent_key]:
                    continue
                for item in self.ling_info[ent_key][ling_key]:
                    
                    item = item.text.lower()
                    if item.lower() in freq:
                        continue
                    if item in freq[ent_key][ling_key]:
                        freq[ent_key][ling_key][item] += 1
                    else:
                        freq[ent_key][ling_key][item] = 1
        return freq
        
    def get_total_analysis_numbers(self):
        # ling_info = self.get_all_doc_ent_ling_info()
        freq = { e: {
                'TOTAL': len(self.ling_info[e]['SENT']),
                'ASSOCIATED_WORDS':len(self.ling_info[e]['DESC_NEIGHBORS']),
                'UNIQUE_ASSOCIATED_WORDS': len(list(set(self.ling_info[e]['DESC_NEIGHBORS'])))
            }
            for e in self.ling_info
        }
        return freq
    
    def get_main_sorted_ents(self):

        freq = self.get_total_analysis_numbers()
        sorted_keys_by_value = [key for key, value in sorted(freq.items(), key=lambda item: item[1]['TOTAL'],reverse=True)]
        res = []
        for item in sorted_keys_by_value:
            if len(item) > 2:
                res.append(item)
            elif freq[item]['TOTAL'] > 2:
                res.append(item)

        return res
    

    def get_ner_widgets(self):
        keys = self.get_main_sorted_ents()

        if len(keys) > 4:
            keys = keys[:4]

        drop_down_entity = widgets.Dropdown(
            options=keys,
            value=keys[0],
            description='Entity',
            disabled=False
        )


        key_labels = [label for label in self.widget_labels]

        drop_down_descriptor = widgets.Dropdown(
            options=key_labels,
            value=key_labels[0],
            description='Descriptor',
            disabled=False
        )

        truncate = widgets.Text(
            value='10',
            placeholder='10',
            description='Maximum results',
            disabled=False   
        )
        return drop_down_entity,drop_down_descriptor,truncate
    
    def make_data_table(self,drop_down_entity,drop_down_descriptor,truncate):
        analysis = self.get_data_analysis()
        items = analysis[drop_down_entity]
        label = self.widget_labels[drop_down_descriptor]
        curr_dictionary = items[label]
        sort_keys = [key for key,value in sorted(curr_dictionary.items(), key=lambda item: item[1],reverse=True) if len(key) > 2]
        total = len(sort_keys)
            
        if total > int(truncate):
            sort_keys = sort_keys[:int(truncate)]
            total = int(truncate)

        print(f"\nDisplaying: {total} results for {drop_down_entity}\n")
        # Create a list of data for your single column
        data = { drop_down_descriptor: sort_keys,
                f"Total Appearances":[curr_dictionary[key] for key in sort_keys]
            }

        df = pd.DataFrame(data)

        # Display the DataFrame
        return df
    
    def render_doc(self):
        return displacy.render(self.ner_doc, style="ent")