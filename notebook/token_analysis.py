import spacy

class DualDocAnalysis:
    def __init__(self,ling_doc,ent_doc):
        self.ling_doc = ling_doc
        self.ent_doc = ent_doc
        self.freq = {}
        self.main_entities = []
        self.set_main_ents(ent_doc)

    def set_main_ents(self,ent_doc):
        if len(self.freq) == 0:
            self.freq = {e.text.lower(): 0 for e in ent_doc.ents}
            
            for e in ent_doc.ents:
                self.freq[e.text.lower()] += 1            
        # analyze entities that appear more than 1 times.
        # project's use case expects the input contains several listings of a single product
        self.main_entities = [e for e in ent_doc.ents if self.freq[e.text.lower()] > 1]
        
    def get_all_doc_ent_ling_info(self):
        if self.main_entities == []:
            self.set_main_ents()

        ling_info = {e.text.lower(): {
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
            ling_info[lower_token_text] = self.get_ling_token_info(token,ling_info[lower_token_text])
            
        return ling_info
            
    def get_ling_token_info(self,token,dic):
        dic['SENT'].append(token.sent.text)

        for t in token.sent:
            lower_token = t.text.lower()
            if t.is_punct or len(t.text) == 1 or t.lemma_ == token.lemma_:
                continue
            if t.like_url or t.ent_type_ == 'ORG':
                continue
            elif t.ent_type_ == 'MONEY':
                continue
            elif t.tag_ in ['NN','NNP','VBG']:
                if t.dep_ == 'compound':
                    dic['C_N'].append(t.text)
                else:
                    dic['N'].append(t.text)
            elif t.pos_ == 'ADJ':
                # print(t.tag_,t.tag_,t.text)
                dic['ADJ'].append(t.text)
            elif t.pos_ == 'ADV':
                dic['ADV'].append(t.text)
            
                
        for chunk in token.sent.noun_chunks:
            if token in chunk:
                dic['FULL_NP'].append(chunk)
                for item in chunk:
                    if item.tag_ in ['NN','NNP','VBG']:
                        dic['DESC_NEIGHBORS'].append(item.text)
        return dic