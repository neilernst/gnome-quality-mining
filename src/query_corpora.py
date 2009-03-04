#!/usr/bin/env python
# encoding: utf-8
"""
query_corpora.py
Created by Neil Ernst on 2009-02-06.
"""

import sys
import getopt
import datetime
from MySQLdb.cursors import DictCursor,SSDictCursor
import MySQLdb
from names import Taxonomy

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
    #in boolean mode match is case-insensitive and uses simple boolean keywords, e.g. no modifier = OR, + = AND, - = NOT
    query_string = """select count(*) from data where match(event) against (\'%(key)s\' in boolean mode) and 
                        product = \'%(product)s\' and  msr_date between cast(\'%(year)s-%(q_end)s\' as Datetime) and 
                        cast(\'%(year)s-%(q_start)s\' as Datetime)""" % {"key":keyword, "product":product, "year":year, "q_start":q_start, "q_end":q_end}

    #TODO: query both tables, and add all keywords e.g. select count(*) from data where match(event) against ('usability useful' in boolean mode) and product = 'nautilus' and  msr_date between cast('2001-01' as Datetime) and cast('2004-03' as Datetime)
    
    #trim results that have initial zero values -- assume these are because there is no data in those time frames
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
        
def query_database(product, signifiers):
    """Sends the query"""
    result_lst = []
    signifier_list = ''
    for signifier in signifiers:
        signifier_list = signifier + ' ' + signifier_list
    
    for year in range(1998,2009):
        for quarter in ('q1', 'q2', 'q3', 'q4'):
            print "Getting counts for: " + signifier_list, product, str(year)
            result, total = get_counts(signifier_list, product, quarter, year)
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
    return result_lst
          
def main():
    t = Taxonomy()     
    for signified in t.get_signified(): # e.g. usability, performance, etc
        for product in t.get_products():
            result = query_database(product, t.get_signifiers(signified)) #e.g. usability: usability, usable, etc.
            print 'finished ' + product + ' ' + signified
            import generate_plots
            generate_plots.main(result, product, signified, normalized=False) #create the plot

if __name__ == "__main__":
    sys.exit(main())


