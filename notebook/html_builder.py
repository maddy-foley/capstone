#Custom HTML Builder to visualize entity spans

class HTMLBuilder:
    def __init__(self,input):
        self.input = input

    def make_string(self,spans):
        string = ""
        string = self.input
        return string