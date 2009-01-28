from datetime import datetime
from MySQLdb.cursors import DictCursor,SSDictCursor
import MySQLdb, getopt, sys
from xml.sax import ContentHandler, parse, parseString,SAXParseException
import re, codecs
from detect_encode import detectXMLEncoding
#from stripInvalidChars import stripNonValidXMLCharacters
from string import upper
from base_classes import Parser, GnomeDataObject

class BugParser(Parser):
    """ Parses bugzilla logs and creates GnomeDataObjects for each event"""
        
    def load_file(self, filename):
        """ Parse an XML-formatted Bugzilla output file"""
        self.ch = BugContentHandler()
        #parseString(filename, self.ch)
        #fileObj = codecs.open( filename, "r", "utf-8" )
        fileObj = open(filename, "r")
        u = fileObj.read() # Returns a Unicode string from the UTF-8 bytes in the file
        # Strip the BOM from the beginning of the Unicode string, if it exists
        #u.lstrip( unicode( codecs.BOM_UTF8, "utf8" ) )

    	parseString(u, self.ch)

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
    
    def set_product(self, name):
        """allows us to specify which product we are parsing. Not used here, as bug list contains all products."""
        self.product_name = name
        
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
            pass
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
        if self.current == "bug_id":
#            if not white.match(content.lstrip()):
            print content.strip().replace(' ', '') 
        if self.current == "product":
            content = content.replace(' ', '') 
            if upper(content) in self.products: 
                self.isProduct = True            
        if self.isProduct: # only for our product of interest. 
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
                                date = datetime.date(1900, 01, 01) 
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
        self.products = ["EKIGA", "DESKBAR-APPLET", "TOTEM", \
                        "EVOLUTION", "METACITY", "EVINCE", "EMPATHY", "NAUTILUS"]
        self.isComment = False
        self.current = "none"
        self.gdo = None
        self.saveLine = ""
        self.bugCount = 0
            
if __name__ == "__main__":
    p = BugParser()
    try:
        options, args = getopt.getopt(sys.argv[1:], "f:p:")
    except getopt.GetoptError, err:
            # print help information and exit:
            print str(err) # will print something like "option -a not recognized"
            sys.exit(2)
    file_name = None
    product = None
    for o,a in options:
        if o == "-f":
            file_name = a
        elif o == "-p":
            product = a
        else:
            assert False, "unhandled option"
    if file_name != None and product != None:
        p.set_product(product)
        p.load_file(file_name)   
        for data in p.get_data():
            print unicode(data)
    #s.load_file('/home/nernst/workspaces/workspace-gany/msr/data/out_gnome.xml')
#    print len(s.get_data())
#    fp = open('/home/nernst/workspaces/workspace-gany/msr/data/gb_clean.xml')
    #fp = open('/home/nernst/workspaces/workspace-gany/msr/data/out.xml')
#    stripped = stripNonValidXMLCharacters(fp)
#    s.load_file(stripped)
#    r = detectXMLEncoding(fp)
#    print r
