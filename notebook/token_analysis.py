import spacy

class DualDocAnalysis:
    def __init__(self,ling_doc,ent_doc):
        self.ling_doc = ling_doc
        self.ent_doc = ent_doc
        self.freq = {}
        self.main_entities = []
        self.set_ents(ent_doc)
        self.ling_info = {}
        self.get_all_doc_ent_ling_info()

    def set_ents(self,ent_doc):
        if len(self.freq) == 0:
            self.freq = {e.text.lower(): 0 for e in ent_doc.ents}
            
            for e in ent_doc.ents:
                self.freq[e.text.lower()] += 1            
        # analyze entities that appear more than 1 times.
        # project's use case expects the input contains several listings of a single product
        self.main_entities = [e for e in ent_doc.ents if self.freq[e.text.lower()] > 1]

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
            token = self.ling_doc[ent.start]
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