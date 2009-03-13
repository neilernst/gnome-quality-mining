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
    
    def characters(self, content):

        bugFormat = re.compile('\d+')
        if self.isBugId:
            bug_id = bugFormat.search(content)
            if bug_id != None:
                self.bug_number = bug_id.group()
                print "Parsing bug # " + str(self.bug_number)
                if self.bug_number == self.bug_to_find:
                    # do something with this bug
                    self.found = True
                    print "Found bug id " + self.bug_number
        
        if self.current == 'product':
            prodFormat = re.compile('\w+.*\w') # a Gnome product name starts with a character and has anything else following and       
            prodmatch = prodFormat.search(content) #ends with a alphanumeric
            if prodmatch != None:
                prodname = prodmatch.group()#.strip()
                if found:
                    #this is a bug whose product we wish to change.
                    pass
                if upper(prodname) in self.products: 
                    self.isProduct = True    
                    self.cur_product = prodname
                else:
                    self.isProduct = False                

    def set_bug_to_find(self, bug):
        self.bug_to_find = bug
        
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.data = open('out.txt', 'w')
        self.isProduct = False 
        self.isBugId = False
        self.isComment = False #SAX element flags
        self.products = [u'EKIGA', u'DESKBAR-APPLET', u'TOTEM', \
                        u'EVOLUTION', u'METACITY', u'EVINCE', u'EMPATHY', u'NAUTILUS']
        self.current = "none"
        self.cur_product = ''
        self.gdo = None
        self.saveLine = ""
        self.bugCount = 0
        self.buffer = ''
        self.bug_number = 0
        self.found = False
            
if __name__ == "__main__":
    try:
        options, args = getopt.getopt(sys.argv[1:], "f:n:")
    except getopt.GetoptError, err:
            # print help information and exit:
            print str(err) # will print something like "option -a not recognized"
            sys.exit(2)
    file_name = None
    bug_to_find = '-1'
    for o,a in options:
        if o == "-f":
            file_name = a
        elif o == "-n":
            bug_to_find = a
        else:
            assert False, "unhandled option"
    if file_name != None and bug_to_find != -1:
        ch = BugContentHandler()
        ch.set_bug_to_find(bug_to_find)
        xml.sax.parse(file_name, ch) 

