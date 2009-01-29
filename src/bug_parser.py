import datetime
from MySQLdb.cursors import DictCursor,SSDictCursor
import MySQLdb
import getopt
import sys
import xml.sax
import re, codecs
from detect_encode import detectXMLEncoding
from string import upper
from base_classes import Parser, GnomeDataObject

class BugParser(Parser):
    """ Parses bugzilla logs and creates GnomeDataObjects for each event"""
        
    def load_file(self, filename):
        """ Parse an XML-formatted Bugzilla output file"""
        self.ch = BugContentHandler()
        #parseString(filename, self.ch)
        #fileObj = codecs.open( filename, "r", "iso-8859-1", 'replace' )
        #fileObj = open(filename, "r")
        #u = fileObj.read() # Returns a Unicode string from the UTF-8 bytes in the file
        # Strip the BOM from the beginning of the Unicode string, if it exists
        #u.lstrip( unicode( codecs.BOM_UTF8, "utf8" ) )
    	xml.sax.parse(filename, self.ch)
        #fileObj.close()
        
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
        
class BugContentHandler(xml.sax.ContentHandler):
    """ a content handler for SAx that processes Gnome bugzilla xml events"""  
    
    def startDocument(self):
        print "Beginning parsing"
    
    def endDocument(self):
        print "Parsing complete"
    
    def startElement(self, name, attrs):
        self.current = name
        if name == "bug_id": # the high-level element
            self.isBugId = True
        if name == "comment":
            self.isComment = True
            self.saveLine = ""
            if self.isProduct:
                self.gdo = GnomeDataObject(GnomeDataObject.BUG) # a new GDO 
                self.gdo.setRSN(self.bug_number)# approximate, might be off by a few
        if name == 'product':
            pass
        if name == 'text':
            self.buffer = '' #an empty buffer for each text element
        if name == 'bug_when':
            self.buffer = '' #an empty buffer for each text element
                      
    def endElement(self, name):
        if name == "bug_id":
            self.isBugId = False
        if name == 'bug':
            self.isProduct = False # reset if set to true from last bug 
        if name == 'product':
            pass
        if name == "comment":
            self.isComment = False
            self.saveLine = ""
            if self.isProduct:
                out_string = unicode(self.gdo)
                self.data.write("\n\n\n******************* new bug report *****************************\n\n\n")
                self.data.write(out_string.encode('iso-8859-1', 'replace')) # we've parsed a bug, so add the completed bug event to our list....
                
        if name == 'text' and self.isProduct and self.isComment:
            event = self.buffer.replace('\n', '').strip()
            self.gdo.setEvent(event)
            self.buffer = ''
        if name == 'bug_when' and self.isProduct and self.isComment:
            dateFormat = re.compile('[\d\-:]+.+[\d\-:]') # a date is any word that starts with a digit, : or -, 
            mat_obj = dateFormat.search(self.buffer) #has stuff in the middle, and ends with a digit. : or -
            if mat_obj != None:
                try: 
                    date = datetime.datetime.strptime(mat_obj.group(), '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    print 'Error on bug date in current bug'
                    date = datetime.date(1900, 01, 01) 
            self.gdo.setDate(date)
            self.buffer = ''
    
    def characters(self, content):
        if self.isProduct and (self.current == 'bug_when' or self.current == 'text'):
        #if self.current == 'bug_when' or self.current == 'text' or self.current == 'product':
            self.buffer = self.buffer + ' ' + content #performance: this is creating a lot of string objects

        bugFormat = re.compile('\d+')
        if self.isBugId:
            bug_id = bugFormat.search(content)
            if bug_id != None:
                self.bug_number = bug_id.group()
                print "Parsing bug # " + str(self.bug_number)
        
        if self.current == 'product':
            prodFormat = re.compile('\w+.*\w') # a Gnome product name starts with a character and has anything else following and       
            prodmatch = prodFormat.search(content) #ends with a alphanumeric
            if prodmatch != None:
                prodname = prodmatch.group()#.strip()
                #print upper(prodname)
                #print "EVOLUTION"
                if upper(prodname) in self.products: 
                    self.isProduct = True    #TODO make sure this detects our product correctly 
                else:
                    self.isProduct = False
            
    def get_data(self):
        return self.data                    
            
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.data = open('out.txt', 'w')
        self.isProduct = False 
        self.isBugId = False
        self.isComment = False #SAX element flags
        self.products = [u'EKIGA', u'DESKBAR-APPLET', u'TOTEM', \
                        u'EVOLUTION', u'METACITY', u'EVINCE', u'EMPATHY', u'NAUTILUS']
        self.current = "none"
        self.gdo = None
        self.saveLine = ""
        self.bugCount = 0
        self.buffer = ''
        self.bug_number = 0
            
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
        #print str(len(p.get_data())) + " data elements captured."
        #for data in p.get_data():
            
            #out.write(data)
            #print unicode(data)
            
            
    #s.load_file('/home/nernst/workspaces/workspace-gany/msr/data/out_gnome.xml')
#    print len(s.get_data())
#    fp = open('/home/nernst/workspaces/workspace-gany/msr/data/gb_clean.xml')
    #fp = open('/home/nernst/workspaces/workspace-gany/msr/data/out.xml')
#    stripped = stripNonValidXMLCharacters(fp)
#    s.load_file(stripped)
#    r = detectXMLEncoding(fp)
#    print r
