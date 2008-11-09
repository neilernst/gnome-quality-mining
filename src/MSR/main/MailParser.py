from MySQLdb.cursors import DictCursor,SSDictCursor
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
        """ connect to the db. Uses DictCursor -- dictionary returned"""
        self.db = MySQLdb.connect(passwd=self.PASSWORD, db=db_name, cursorclass=DictCursor)
        self.cursor = self.db.cursor()

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
        print node.getEvent()
        self.data.append(node)
    
    def __init__(self):
        Parser.__init__(self)
        self.cursor = None
        self.db = None
        self.data = []
    
if __name__ == '__main__':
    p = MailParser()
    p.load_file("deskbar-mail")
    p.query("Select message_body, first_date, subject from messages")
    print p.return_data()[2]
    