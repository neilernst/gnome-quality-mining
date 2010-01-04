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
    prod = 'Nautilus'
    total = 50
    query_string = """ select event from data_objects.refsq_data 
     order by rand() limit %(total)d"""  % {"prod":prod, "total":total} # msr_type = "Mail" where product = "%(prod)s" 
    # = """select event from data_objects.refsq_data where match(event) 
                  #  against (\'%(key)s\' in boolean mode)
                  #  order by rand() limit %(total)d"""  % {"key":keyword, "total":total}
    
    try:
        # print query_string
        store_cursor.execute(query_string)
        yes = 0.0
        no = 0.0
        i = 0
        wn_fn_count = 0
        ext_fn_count = 0
        for result in store_cursor.fetchall():
            event = result.values()[0]
            #result = str(store_cursor.fetchall().values()[0]) #{'count(*)': 6L} dict
            print event
            i = i + 1
            answer = raw_input("\n******\n"+ str(i) + "/" + str(total) + " Quality: [u/r/m/e/p/f/n]: ")
            #wait for user input
            if answer != 'n':
                yes = yes + 1.0
                #check against our algorithm
                if answer == 'u':
                    signifiers_ext = t.get_signifiers('Usability')
                    signifiers_wn = t.get_signifiers_wn('Usability')
                    #print signifiers
                elif answer == 'r':
                    signifiers_ext = t.get_signifiers('Reliability')
                    signifiers_wn = t.get_signifiers_wn('Reliability')
                elif answer == 'm':
                    signifiers_ext = t.get_signifiers('Maintainability')
                    signifiers_wn = t.get_signifiers_wn('Maintainability')
                elif answer == 'e':
                    signifiers_ext = t.get_signifiers('Efficiency')
                    signifiers_wn = t.get_signifiers_wn('Efficiency')
                elif answer == 'p':
                    signifiers_ext = t.get_signifiers('Portability')
                    signifiers_wn = t.get_signifiers_wn('Portability')
                elif answer == 'f':
                    signifiers_ext = t.get_signifiers('Functionality')            
                    signifiers_wn = t.get_signifiers_wn('Functionality')            

                found_wn, found_ext = check_list(event, signifiers_wn, signifiers_ext)
                if not found_wn:
                    # false negative
                    wn_fn_count += 1  
                    print wn_fn_count
                if not found_ext:
                    ext_fn_count += 1
                    print ext_fn_count          
            else:
                no = no + 1.0 # TODO could extend this to see whether the standard query matches it even so 
        wn_rate = wn_fn_count/float(yes)
        ext_rate = ext_fn_count/float(yes) #of the ones we marked, how many were not found?
        print ext_fn_count
        print "Number of matches was %s" % (yes)
        print "False negative rate was wn: %s and ext: %s" % (str(wn_rate),str(ext_rate))
    except (ValueError):
        print 'Error in query syntax'   

def check_list(event, signifiers_wn, signifiers_ext):
    """ check a keyword list against a message to see if there is a match"""
    wn_found = False
    ext_found = False
    for sig in signifiers_wn:
        #find an occurrence in the 'event'
        pat = '\W*'+sig+'\W*'
        match_obj = re.compile(pat, re.IGNORECASE)
        match = match_obj.search(event)
        #print match
        if match != None:
            wn_found = True 
            break
    for sig in signifiers_ext:
        #find an occurrence in the 'event'
        pat = '\W*'+sig+'\W*'
        match_obj = re.compile(pat, re.IGNORECASE)
        match = match_obj.search(event)
        #print match
        if match != None:
            ext_found = True 
            break
    
    return wn_found, ext_found
                
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


