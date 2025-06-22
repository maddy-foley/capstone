from typing import Optional

class TradingData:
     def __init__(self,text:str,start_idx:int,end_idx: int,label:str,attr:Optional[list]):
          self.text = text
          self.start_idx = start_idx
          self.end_idx = end_idx
          self.label = label
          self.attr = attr

    def get_