from MSR.main.Parser import Parser
from xml.dom import minidom
from MSR.main.GnomeDataObject import GnomeDataObject
from datetime import datetime
from xml.sax import ContentHandler, parse

class BugParser(Parser):
    """ Parses bugzilla logs and creates GnomeDataObjects for each event"""
        
    def load_file(self, filename):
        """ Parse an XML-formatted SVN output file"""
#        bugfile = open(filename)
#        self.f = minidom.parse(bugfile)
#        bugfile.close()
        ch = BugContentHandler()
        parse(filename, ch)
        
        
    
    def parse_line(self):
        """ parse the entries in the log file, add them to the list of GDOs"""
        entries = self.f.getElementsByTagName('bug')
        for entry in entries:
            if entry.childNodes[3].hasChildNodes():
                bug_date = entry.ChildNodes[4].childNodes[0].data
                bug_date = bug_date[5:28] # strip the \n junk
                bug_date = datetime.strptime(bug_date, '%Y-%m-%d %H:%M:%S')
                
            if entry.childNodes[7].hasChildNodes():
                strdate = entry.childNodes[3].childNodes[0].data
                strdate = strdate[0:19] #this removes the milliseconds and TZ info
                date = datetime.strptime(strdate, '%Y-%m-%dT%H:%M:%S') 
                msg = entry.childNodes[7].childNodes[0].data # DOM TextNode containing log message. Hard-coding == bad
            n = GnomeDataObject(GnomeDataObject.SVN)
            n.setDate(date)
            #n.setRSN(revNum)
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
        
class BugContentHandler(ContentHandler):
    """ a content handler for SAx that processes Gnome bugzilla xml events"""
    
    CURRENT = "none"
    
    def startDocument(self):
        pass
    
    def endDocument(self):
        pass
    
    def startElement(self, name, attrs):
        #print "Starting: " + name
        if name == "product":
            self.CURRENT = name
        else:
            self.CURRENT = "none"
        
    def endElement(self, name):
        #print "Ending: " + name
        pass 
    
    def ignorableWhitespace(self,whitespace):
        pass
    
    def characters(self,content):
        if self.CURRENT == "product":
            print content
            
if __name__ == "__main__":
    s = BugParser()
    #s.load_file('/home/nernst/workspaces/workspace-gany/msr/data/gnome_bugzilla.xml')
    s.load_file('/home/nernst/workspace/msr/src/MSR/tests/sample-data/bugzilla-test.xml')   
    #s.parse_line()   
   # assert(len(s.get_data()) == 781)
