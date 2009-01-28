from Parser import Parser
from MySQLdb.cursors import DictCursor,SSDictCursor
import MySQLdb, getopt, sys
from xml.dom import minidom
from xml.etree import ElementTree
from GnomeDataObject import GnomeDataObject
from datetime import datetime

class SVNParser(Parser):
    """ Parses SVN logs and creates GnomeDataObjects for each event"""
        
    PASSWORD = "hello"
    
    def load_file(self, filename):
        """ Parse an XML-formatted SVN output file"""
        svnfile = open(filename)
        #self.f = minidom.parse(svnfile)
        self.f = ElementTree.parse(svnfile)
        svnfile.close()
         
    def parse_line(self):
        """ parse the entries in the log file, add them to the list of GDOs"""
        #entries = self.f.getElementsByTagName('logentry')
        iter = self.f.getiterator('logentry')
        for entry in iter:
            revNum = entry.attrib.get('revision') 
            strdate = entry.find('date').text
            strdate = strdate[0:19] #this removes the milliseconds and TZ info
            date = datetime.strptime(strdate, '%Y-%m-%dT%H:%M:%S') 
            try: 
                msg = entry.find('msg').text
            except AttributeError:
                msg = ""
            n = GnomeDataObject(GnomeDataObject.SVN)
            n.setDate(date)
            n.setRSN(revNum)
            n.setEvent(msg)
            self.store_tokens(n)
            
    #def store_tokens(self, node):
    #    self.data.append(node)
        
    def connect_store(self, db_name):
        """ connect to store the data"""
        self.storedb = MySQLdb.connect(passwd=self.PASSWORD, db=db_name, cursorclass=DictCursor)
        self.store_cursor = self.storedb.cursor()
                    
    def store_tokens(self, node):
        """ store in the database"""
        store_con = self.connect_store(Parser.STORAGE_DB)
        #print node.getEvent()
        #store_query_string = "INSERT INTO %s (rsn, date, type, event) VALUES (%i, %s, %s, %s)" % \  (Parser.STORAGE_TABLE, node.getRSN(), node.getDate(), node.getType(), node.getEvent())
        try:
            self.store_cursor.execute("INSERT INTO data (rsn, msr_date, msr_type, event, product) VALUES (%s, %s, %s, %s, %s)", \
            (node.getRSN(), node.getDate(), node.getType(), node.getEvent(), self.product_name) )
        except (ValueError):
            print 'Error in query syntax'  
             
    def set_product(self, name):
        """allows us to specify which product we are parsing"""
        self.product_name = name
            
    def get_data(self):
        return self.data
            
    def __init__(self):
        Parser.__init__(self)
        self.f = None
        self.data = [] # a list of GDOs with the parsed data
            
if __name__ == "__main__":
    #s = SVNParser()
    #s.load_file('sample-data/totem.xml')   
    #assert(len(s.get_data()) == 781)
    p = SVNParser()
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
        p.parse_line()   
