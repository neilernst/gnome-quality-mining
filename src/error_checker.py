""" Generates random records from the corpora to assess error rates"""

import sys
import getopt
import datetime
from MySQLdb.cursors import DictCursor,SSDictCursor
import MySQLdb

def connect_corpus(db_name):
    """ connect to db"""
    storedb = MySQLdb.connect(passwd="hello", db=db_name, cursorclass=DictCursor)
    store_cursor = storedb.cursor()
    return store_cursor
    
def get_counts(keyword):
    """ store in the database"""
    store_cursor = connect_corpus("data_objects")

    
    query_string = """select event from data_objects.data where match(event) 
                    against (\'%(key)s\' in boolean mode) order by rand() limit 20"""  % {"key":keyword}
    
    try:
        store_cursor.execute(query_string)
        for result in store_cursor.fetchall():
        #result = str(store_cursor.fetchall().values()[0]) #{'count(*)': 6L} dict
            print result.values()[0]
            answer = raw_input("******\nRelevant (y/n): ")
            #wait for user input
            #y for relevant, N for irrelevant
            yes = 0.0
            no = 0.0
            if answer == 'y':
                yes = yes + 1.0
            else:
                no = no + 1.0
        rate = yes/20.0
        print "Error rate for term %s was: %s" % (keyword, str(rate))
    except (ValueError):
        print 'Error in query syntax'   
               
def main():
   get_counts('usability')

if __name__ == "__main__":
    sys.exit(main())
