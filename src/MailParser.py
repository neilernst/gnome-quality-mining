from MySQLdb.cursors import DictCursor,SSDictCursor
import MySQLdb
#from MySQLdb.Exceptions import MySQLError
from Parser import Parser
from GnomeDataObject import GnomeDataObject

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
		self.storedb = MySQLdb.connect(passwd=self.PASSWORD, db=Parser.STORAGE_DB, cursorclass=DictCursor)
		self.store_cursor = self.storedb.cursor()

    def query(self, query_string):
        """ get all the rows in the db """
        self.cursor.execute(query_string)
        result_list = self.cursor.fetchall()
        for r in result_list:
            date = r['first_date']
            subj = r['subject']
            body = r['message_body']  
            text = subj + body 
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
    
    def store_tokens(self, node):
		""" store in the database"""
		store_query_string = 'INSERT INTO %s (rsn, date, type, event) VALUES (%i, %s, %s, %s)' % \
									(Parser.STORAGE_TABLE, node.getDate(), node.getType(), node.getEvent())
		try:
			self.store_cursor.execute(store_query_string)
		except (Error):
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
    p.load_file("fm3_nautilus_mls")
    p.query("Select message_body, first_date, subject from messages")
    print p.return_data()[2]
    