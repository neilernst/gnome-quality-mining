from Parser import Parser
from xml.dom import minidom
from GnomeDataObject import GnomeDataObject
from datetime import datetime

class SVNParser(Parser):
    """ Parses SVN logs and creates GnomeDataObjects for each event"""
    
        
    def load_file(self, filename):
        """ Parse an XML-formatted SVN output file"""
        svnfile = open(filename)
        self.f = minidom.parse(svnfile)
        svnfile.close()
        
    
    def parse_line(self):
        """ parse the entries in the log file, add them to the list of GDOs"""
        entries = self.f.getElementsByTagName('logentry')
        for entry in entries:
            revNum = entry.attributes['revision'].value
            if entry.childNodes[7].hasChildNodes():
                strdate = entry.childNodes[3].childNodes[0].data
                strdate = strdate[0:19] #this removes the milliseconds and TZ info
                date = datetime.strptime(strdate, '%Y-%m-%dT%H:%M:%S') 
                msg = entry.childNodes[7].childNodes[0].data # DOM TextNode containing log message. Hard-coding == bad
            n = GnomeDataObject(GnomeDataObject.SVN)
            n.setDate(date)
            n.setRSN(revNum)
            n.setEvent(msg)
            self.store_tokens(n)
            
    def store_tokens(self, node):
        self.data.append(node)
        
    def get_data(self):
        return self.data
            
    def __init__(self):
        Parser.__init__(self)
        self.f = None
        self.data = [] # a list of GDOs with the parsed data
            
if __name__ == "__main__":
    s = SVNParser()
    s.load_file('/home/nernst/workspace/msr/src/MSR/tests/sample-data/totem.xml')   
    s.parse_line()   
    assert(len(s.get_data()) == 781)
