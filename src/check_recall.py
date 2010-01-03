""" Generates random records from the corpora to assess error rates"""

import sys, re
import getopt
import datetime
from MySQLdb.cursors import DictCursor,SSDictCursor
import MySQLdb
from names import Taxonomy


def connect_corpus(db_name):
    """ connect to db"""
    storedb = MySQLdb.connect(passwd="happy1", db=db_name, cursorclass=DictCursor)
    store_cursor = storedb.cursor()
    return store_cursor
    
def get_counts(keyword):
    """ store in the database"""
    store_cursor = connect_corpus("data_objects")
    t = Taxonomy()
    
    total = 5 
    query_string = """select event from data_objects.refsq_data where product = "Nautilus" 
    and msr_type = "Mail" order by rand() limit 50
    """
    # = """select event from data_objects.refsq_data where match(event) 
                  #  against (\'%(key)s\' in boolean mode)
                  #  order by rand() limit %(total)d"""  % {"key":keyword, "total":total}
    
    try:
        # print query_string
        store_cursor.execute(query_string)
        yes = 0.0
        no = 0.0
        i = 0
        for result in store_cursor.fetchall():
            fn_count = 0
        #result = str(store_cursor.fetchall().values()[0]) #{'count(*)': 6L} dict
            print result.values()[0]
            i = i + 1
            answer = raw_input("\n******\n"+ str(i) + "/50 Quality: [U/R/M/E/P/F/N]: ")
            #wait for user input
            #y for relevant, N for irrelevant
            if answer != 'N':
                yes = yes + 1.0
                #check against our algorithm
                if answer == 'U':
                    signifiers = t.get_signifiers_wn('Usability')
                    missed == True
                    for sig in signifiers:
                        #find an occurrence in the 'event'
                        match = re.search('\s'+sig+'\s',result)
                        if match != None:
                            missed = False # we missed one
                    if missed == True:
                        # false negative
                        fn_count += 1
            else:
                no = no + 1.0 # TODO could extend this to see whether the standard query matches it even so 
        rate = fn_count/float(total)
        print "Number of matches was %s" % (yes)
        print "False positive rate for term %s was: %s" % (keyword, str(rate))
    except (ValueError):
        print 'Error in query syntax'   
               
def main():
   t = Taxonomy()
   # signifiers = t.get_signifiers('Efficiency') #extended lists
   signifiers = t.get_signifiers_wn('Usability') # wordnet lists
   signifier_list = ''
   for signifier in signifiers:
       signifier_list = signifier + ' ' + signifier_list
   get_counts(signifier_list)

if __name__ == "__main__":
    sys.exit(main())


