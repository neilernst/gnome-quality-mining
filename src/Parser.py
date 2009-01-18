# this is an abstract parser object
# it loads a text file
# parses the line
# and stores the tokens somehow

class Parser(object):
    
STORAGE_TABLE = "data"
    STORAGE_DB = "data_objects"

    def load_file(self, filename):
        pass
    
    def parse_line(self):
        pass
    
    def store_tokens(self, node):
        pass
    
    def __init__(self):
        pass