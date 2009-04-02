from MySQLdb.cursors import DictCursor,SSDictCursor
import MySQLdb
import _mysql_exceptions
from base_classes import GnomeDataObject, Parser
import getopt,sys

# the Mail data is in MySql dumps. We will use the subject and body as our corpus, and the date of sending as the date. We can't directly determine 
# RSN.
# See http://mysql-python.sourceforge.net/MySQLdb.html#some-examples

class MailParser(Parser):
    """ Parses mail logs and creates GnomeDataObjects for each event"""
    
    PASSWORD = "hello"
    TABLE = "messages"
    
    def connect(self, db_name):
        """ connect to the db. Uses DictCursor -- dictionary returned"""
        self.db = MySQLdb.connect(passwd=self.PASSWORD, db=db_name, cursorclass=DictCursor)
        self.cursor = self.db.cursor()

    def connect_store(self, db_name):
        """ connect to store the data"""
        self.storedb = MySQLdb.connect(passwd=self.PASSWORD, db=db_name, cursorclass=DictCursor)
        self.store_cursor = self.storedb.cursor()

    def query(self, query_string):
        """ get all the rows in the db """
        self.cursor.execute(query_string)
        result_list = self.cursor.fetchall()
        for r in result_list:
            date = r['first_date']
            subj = r['subject']
            body = r['message_body']  
            text = subj + ' ' + body 
            node = GnomeDataObject(GnomeDataObject.MAIL)  
            node.setDate(date)
            node.setEvent(text)
            node.setRSN(-1) #-1 indicates no RSN retrieved
            self.store_tokens(node)
        self.cursor.close()
          
    def return_result(self):
        """ for testing"""
    
    def return_data(self):
        return self.data
    
    def load_file(self, filename):
        """ call connect to fill contract"""
        self.connect(filename)
    
    def parse_line(self):
        """ generic query to fill contract"""
        self.query("SELECT * FROM" + self.TABLE)
        
    def set_product(self, name):
        """allows us to specify which product we are parsing"""
        self.product_name = name
    
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
    
    def __init__(self):
        Parser.__init__(self)
        self.cursor = None
        self.db = None
        self.store_cursor = None
        self.store_db = None
        self.data = []
    
if __name__ == '__main__':
    p = MailParser()
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
        p.query("Select message_body, first_date, subject from messages")
    #print p.return_data()[2]
    
