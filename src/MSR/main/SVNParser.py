from MSR.main.Parser import Parser
from xml.dom import minidom
from MSR.main.GnomeDataObject import GnomeDataObject

class SVNParser(Parser):
    """ Parses SVN logs and creates GnomeDataObjects for each event"""
    
    f = None
    data = [] # a list of GDOs with the parsed data
    
    def loadFile(self, file):
        """ Parse an XML-formatted SVN output file"""
        self.f = minidom.parse(file)
    
    def parseLine(self):
        """ parse the entries in the log file, add them to the list of GDOs"""
        entries = self.f.getElementsByTagName('logentry')
        for entry in entries:
            revNum = entry.attributes['revision'].value
            if entry.childNodes[7].hasChildNodes():
                msg = entry.childNodes[7].childNodes[0] # DOM TextNode containing log message. Hard-coding == bad
            n = GnomeDataObject(GnomeDataObject.SVN)
            #n.setDate()
            n.setRSN(revNum)
            n.setEvent(msg)
            self.storeTokens(n)
            
    def storeTokens(self, node):
        self.data.append(node)
        
    def getData(self):
        return self.data
            
if __name__ == "__main__":
    s = SVNParser()
    s.loadFile('/home/nernst/workspace/msr/src/MSR/tests/sample-data/totem.xml')   
    s.parseLine()   
    print len(s.data)
