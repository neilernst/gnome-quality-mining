from MySQLdb.cursors import Cursor, SSDictCursor
import MySQLdb
from MSR.main.Parser import Parser
from MSR.main.GnomeDataObject import GnomeDataObject

# the Mail data is in MySql dumps. We will use the subject and body as our corpus, and the date of sending as the date. We can't directly determine 
# RSN.
# See http://mysql-python.sourceforge.net/MySQLdb.html#some-examples

class MailParser(Parser):
    """ Parses mail logs and creates GnomeDataObjects for each event"""
    
    PASSWORD = "happy1"
    TABLE = "messages"
    
    def connect(self, db_name):
        """ connect to the db. Uses SSDictCursor -- serverside, dictionary returned"""
        self.db = MySQLdb.connect(passwd=self.PASSWORD,db=db_name, cursorclass=SSDictCursor)

    def query(self, query_string):
        """ get all the rows in the db """
        
        self.c = self.db.cursor()
        self.c.execute(query_string)
        while self.c.fetchone():
            r = self.c.fetchone()
            date = r['first_date']
            subj = r['subject']
            body = r['message_body'] # TODO format is [<email.Message.Message instance at 0xb75f110c>, <email.Message.Message instance at 0xb75f148c>]  
            text = subj + body #TODO must unpickle body?
            node = GnomeDataObject(GnomeDataObject.MAIL)  
            node.setDate(date)
            node.setEvent(text)
            node.setRSN(-1) #-1 indicates no RSN retrieved
            self.store_tokens(node)
        self.c.close()
          
    def return_result(self):
        """ for testing"""
        return self.c.fetchone()
    
    def load_file(self, filename):
        """ call connect to fill contract"""
        self.connect(filename)
    
    def parse_line(self):
        """ generic query to fill contract"""
        self.query("SELECT * FROM" + self.TABLE)
    
    def store_tokens(self, node):
        self.data.append(node)
    
    def __init__(self):
        Parser.__init__(self)
        self.c = None
        self.db = None
        self.data = []
    
if __name__ == '__main__':
    p = MailParser()
    p.load_file("deskbar-mail")
    p.query("Select * from messages")
    print p.return_result()
    