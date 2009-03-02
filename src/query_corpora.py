#!/usr/bin/env python
# encoding: utf-8
"""
query_corpora.py

Created by Neil Ernst on 2009-02-06.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import getopt
import datetime
from MySQLdb.cursors import DictCursor,SSDictCursor
import MySQLdb

help_message = '''
Module to query a database of parsed bug, mail, and svn text
'''

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def connect_corpus(db_name):
    """ connect to db"""
    storedb = MySQLdb.connect(passwd="hello", db=db_name, cursorclass=DictCursor)
    store_cursor = storedb.cursor()
    return store_cursor
    
def get_counts(keyword, product, q, year):
    """ store in the database"""

    store_cursor = connect_corpus("data_objects")

    #Define the start and end of yearly quarters"""
    if q == 'q1':
      q_end = '01-01'
      q_start = '03-31'
    if q == 'q2':
      q_end = '04-01'     #note, these are backward, too lazy to change var name
      q_start = '06-30'
    if q == 'q3':
      q_end = '07-01'
      q_start = '09-30'
    if q == 'q4':
      q_end = '10-01'
      q_start = '12-31'     

    #this query determines number of events for the given keyword  
    query_string = """select count(*) from data where match(event) against (\'%(key)s\' in boolean mode) and 
                        product = \'%(product)s\' and  msr_date between cast(\'%(year)s-%(q_end)s\' as Datetime) and 
                        cast(\'%(year)s-%(q_start)s\' as Datetime)""" % {"key":keyword, "product":product, "year":year, "q_start":q_start, "q_end":q_end}

    #this query determines total events overall (to normalize against)               
    totals_query =  """select count(*) from data where product = \'%(product)s\' and  msr_date between 
                        cast(\'%(year)s-%(q_end)s\' as Datetime) and 
                        cast(\'%(year)s-%(q_start)s\' as Datetime)""" % {"product":product, "year":year, "q_start":q_start, "q_end":q_end}
    try:
        store_cursor.execute(query_string)
        key_num = str(store_cursor.fetchone().values()[0]) #{'count(*)': 6L} dict
        store_cursor.execute(totals_query)
        total_val = store_cursor.fetchone().values()
        total_num = int(str(total_val[0]))
        return int(key_num), total_num
    except (ValueError):
        print 'Error in query syntax'
          
def main(argv=None):
    product = ''
    keyword = ''
    quarter = 'q1'
    year = 2010
    
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hk:p:")
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option == "-k":
                keyword = value
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option == "-p":
                product = value

        result_lst = []
        
        for year in range(1998,2009):
            for quarter in ('q1', 'q2', 'q3', 'q4'):
                result, total = get_counts(keyword, product, quarter, year)
                month = 0
                if quarter == 'q1': 
                    month = 3
                elif quarter == 'q2':
                    month = 6
                elif quarter == 'q3':
                    month = 9
                elif quarter == 'q4':
                    month = 12
                normalized = 0
                if total != 0:
                    normalized = 10000*float(result)/float(total)
                res_tuple = (normalized,result, datetime.date(year,month,30)) #a quarter's date representation is the end of the quarter
                result_lst.append(res_tuple)
        #TODO first, summarize for that signifier (e.g. usability->useful, usable, utility) for each database (data, t_data)
        #then generate the plot for each signifier and product
        import generate_plots
        generate_plots.main(result_lst, product, keyword, normalized=False) #create the plot
        
                
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
#TODO account for misspelinges 

class Taxonomy():
    """ class to store lists of various terms of interest. Each element/term in the list will be queried once."""
    usability_spell = ['usbility', 'useability',]
    usability_syn = ['usability', 'serviceability', 'serviceableness', 'usableness', 'useableness']
    usability_hyper = ['utility', 'usefulness']
    usability_deriv = ['serviceable', 'usable', 'useable']
    usability_meronym = ['Learnability', 'Understandability', 'Operability'] #as defined in iso9126
    self.usability =  usability_syn + usability_hyper + usability_deriv + usability_meronym #+ usability_spell
    
    functionality_spell = []
    functionality_syn = ['functionality']
    functionality_hyper = ['practicality']
    functionality_deriv = ['functional']
    functionality_meronym = ['Suitability', 'Interoperability', 'Accuracy', 'Compliance', 'Security'] #as defined in iso9126
    self.functionality =  functionality_syn + functionality_hyper + functionality_deriv + functionality_meronym #+ _spell
       
    reliability_spell = []
    reliability_syn = ['dependability', 'dependableness', 'reliability', 'reliableness']
    reliability_hyper = ['responsibility', 'responsibleness']
    reliability_deriv = ['dependable', 'reliable']
    reliability_meronym = ['Maturity', 'Recoverability', 'Fault Tolerance'] #as defined in iso9126
    self.reliability =  reliability_syn + reliability_hyper + reliability_deriv + reliability_meronym #+ _spell
    
    maintainability_spell = []
    maintainability_syn = ['maintainable']
    maintainability_hyper = []
    maintainability_deriv = ['maintain']
    maintainability_meronym = ['Stability', 'Analyzability', 'Changeability', 'Testability'] #as defined in iso9126
    self.maintainability =  maintainability_syn + maintainability_hyper + maintainability_deriv + maintainability_meronym #+ _spell
    
    portability_spell = []
    portability_syn = ['portability']
    portability_hyper = ['movability', 'movableness']
    portability_deriv = ['portable']
    portability_meronym = ['Installability', 'Replaceability', 'Adaptability', 'Conformance'] #as defined in iso9126
    self.portability =  portability_syn + portability_hyper + portability_deriv + portability_meronym #+ _spell
    
    # efficiency_spell = []
    #  efficiency_syn = []
    #  efficiency_hyper = []
    #  efficiency_deriv = []
    #  efficiency_meronym = [] #as defined in iso9126
    #  efficiency =  _syn + _hyper + _deriv + _meronym #+ usability_spell
    #efficiency = time/resource behaviour == performance