from MSR.main.Parser import Parser
from MSR.main.GnomeDataObject import GnomeDataObject
from datetime import datetime
from xml.sax import ContentHandler, parse
import re

class BugParser(Parser):
    """ Parses bugzilla logs and creates GnomeDataObjects for each event"""
        
    def load_file(self, filename):
        """ Parse an XML-formatted SVN output file"""
        self.ch = BugContentHandler()
        parse(filename, self.ch)
            
    def parse_line(self):
        pass
            
    def store_tokens(self, node):
        pass

    def get_data(self):
        return self.ch.get_data()
            
    def __init__(self):
        Parser.__init__(self)
        self.f = None
        self.ch = None # a list of GDOs with the parsed data
        
class BugContentHandler(ContentHandler):
    """ a content handler for SAx that processes Gnome bugzilla xml events"""  
    
    def startDocument(self):
        print "Beginning parsing"
    
    def endDocument(self):
        print "Parsing complete"
    
    def startElement(self, name, attrs):
        #print "Starting: " + name
        self.current = name
        if name == "bug": # the high-level element
            self.bugCount += self.bugCount
        if name == "comment":
            self.gdo = GnomeDataObject(GnomeDataObject.BUG) # a new GDO 
            self.gdo.setRSN(-1)# no RSN in these events
            self.isComment = True
            self.saveLine = ""
        
    def endElement(self, name):
        if name == "bug":
            self.isProduct = False # reset if set to true from last bug 
        if name == "comment":
            self.isComment = False
            self.saveLine = ""
            self.data.append(self.gdo) # we've parsed a bug, so add the completed bug event to our list....
    
    def get_data(self):
        return self.data
    
    
    def characters(self,content):
        """ returns the characters inside an element, incl. whitespace"""
        # parse out whitespace
        white = re.compile('\S')
        autoComment = re.compile('\*\*\*.*\*\*\*')  
        if self.current == "product":
            content = content.replace(' ', '') 
            if content in self.products: 
                self.isProduct = True            
        if self.isProduct: # only for our product of interest. Eventually a list.
            if self.isComment:
                if self.current == "bug_when":
                    lines = content.splitlines()
                    for line in lines:
                        line = line.lstrip()
                        if white.match(line):
                            try: 
                                date = datetime.strptime(line, '%Y-%m-%d %H:%M:%S')
                            except ValueError:
                                print 'Error on bug date in bug: ' + str(self.bugCount)
                                date = datetime.today() 
                            self.gdo.setDate(date)
                if self.current == "text":
                    lines = content.splitlines()
                    for line in lines:
                        line = line.lstrip()
                        if white.match(line):
                            if not autoComment.match(line):
                                self.saveLine = self.saveLine + " " + line 
                        self.gdo.setEvent(self.saveLine)
            
    def __init__(self):
        ContentHandler.__init__(self)
        self.data = []
        self.isProduct = False
        self.products = ["ekiga", "deskbar-applet", "totem", "evolution", "metacity", "evolution", "empathy", "nautilus"]
        self.isComment = False
        self.current = "none"
        self.gdo = None
        self.saveLine = ""
        self.bugCount = 0
            
if __name__ == "__main__":
    s = BugParser()
#    s.load_file('/home/nernst/workspaces/workspace-gany/msr/data/gnome_bugzilla.xml')
    s.load_file('/home/nernst/workspace/msr/src/MSR/tests/sample-data/bugzilla-test.xml') 
#    print len(s.get_data())
    for data in s.get_data():
        print data
        pass
