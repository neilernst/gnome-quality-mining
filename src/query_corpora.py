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
    storedb = MySQLdb.connect(user='root', db=db_name, cursorclass=DictCursor, unix_socket='/u/nernst/mysqld.socket')
    store_cursor = storedb.cursor()
    return store_cursor
    
def get_counts(keyword, product):  #, q, year):
    """ store in the database"""
    db_name = 'msr_data'
    store_cursor = connect_corpus(db_name)

    query_string = """SELECT yearweek(msr_date), COUNT(*) FROM t_data WHERE product = \'%(product)s\' 
                        AND MATCH(event) AGAINST (\'%(key)s\' in boolean mode) GROUP BY yearweek(msr_date)
                        UNION ALL 
                        SELECT yearweek(msr_date), COUNT(*) FROM data WHERE product = \'%(product)s\' 
                        AND MATCH(event) AGAINST (\'%(key)s\' in boolean mode)
                        GROUP BY yearweek(msr_date) ASC """ % {"key":keyword, "product":product}

    #this query determines total events overall (to normalize against)                                
    totals_query = """SELECT yearweek(msr_date), COUNT(*) FROM t_data WHERE product = \'%(product)s\' GROUP BY yearweek(msr_date)
                        UNION ALL 
                      select yearweek(msr_date), count(*) from data WHERE product = \'%(product)s\' 
                      group by yearweek(msr_date) ASC """ % {"product":product}
    try:
        store_cursor.execute(query_string)
        key_num = store_cursor.fetchall()
        key_num = create_dict(key_num) #create a dict with date-week as key, count as values
        store_cursor.execute(totals_query)
        total_val = store_cursor.fetchall()
        total_num = create_dict(total_val)
        return key_num, total_num #two tuples
    except (ValueError):
        print 'Error in query syntax'
        
def create_dict(key_dict):
    res_list = []
    for x in key_dict:
        dw = x.values()[0]
        cnt = x.values()[1]
        rdict = {dw: cnt}
        res_list.append(rdict)
    return res_list
    
def query_database(product, signifiers):
    """Sends the query"""
    result_lst = []
    signifier_list = ''
    for signifier in signifiers:
        signifier_list = signifier + ' ' + signifier_list
    
    print "Getting counts for: " + signifier_list, product
    result, total = get_counts(signifier_list, product)#, quarter, year)
    print result, total

    normalized = 0
    if total != 0:
        normalized = 10000*float(result)/float(total)
    res_tuple = (normalized,result, datetime.date(year,month,30)) #use weeknum#a quarter's date representation is the end of the quarter
    result_lst.append(res_tuple)
    return result_lst
          
def save_file(result, product, signified):
    f = file('/u/nernst/msr/data/icsm-pickles/'+product+'-'+ signified + '.pcl', 'wb')
    import pickle
    pickle.dump(result, f)
    f.close()
    
def main():
    t = Taxonomy()     
    for signified in t.get_signified(): # e.g. usability, performance, etc
        for product in t.get_products():
            result = query_database(product, t.get_signifiers(signified)) #e.g. usability: usability, usable, etc.
            #print result
            save_file(result, product, signified)
            #print 'finished ' + product + ' ' + signified
            #import generate_plots
            #generate_plots.main(result, product, signified, normalized=False) #create the plot

if __name__ == "__main__":
    sys.exit(main())

    #Define the start and end of yearly quarters"""
     # if q == 'q1':
     #       q_end = '01-01'
     #       q_start = '03-31'
     #     if q == 'q2':
     #       q_end = '04-01'     #note, these are backward, too lazy to change var name
     #       q_start = '06-30'
     #     if q == 'q3':
     #       q_end = '07-01'
     #       q_start = '09-30'
     #     if q == 'q4':
     #       q_end = '10-01'
     #       q_start = '12-31'     
     #this query determines number of events for the given keyword  
     #in boolean mode match is case-insensitive and uses simple boolean keywords, e.g. no modifier = OR, + = AND, - = NOT
     # query_string = """select count(*) from data where match(event) against (\'%(key)s\' in boolean mode) and 
     #                     product = \'%(product)s\' and  msr_date between cast(\'%(year)s-%(q_end)s\' as Datetime) and 
     #                     cast(\'%(year)s-%(q_start)s\' as Datetime) UNION ALL
     #                     select count(*) from t_data where match(event) against (\'%(key)s\' in boolean mode) and 
     #                     product = \'%(product)s\' and  msr_date between cast(\'%(year)s-%(q_end)s\' as Datetime) and 
     #                     cast(\'%(year)s-%(q_start)s\' as Datetime)""" % {"key":keyword, "product":product, "year":year, "q_start":q_start, "q_end":q_end}

     # totals_query =  """select count(*) from data where product = \'%(product)s\' and  msr_date between 
     #                     cast(\'%(year)s-%(q_end)s\' as Datetime) and 
     #                     cast(\'%(year)s-%(q_start)s\' as Datetime) UNION ALL
     #                     select count(*) from t_data where product = \'%(product)s\' and  msr_date between 
     #                     cast(\'%(year)s-%(q_end)s\' as Datetime) and 
     #                     cast(\'%(year)s-%(q_start)s\' as Datetime)""" % {"product":product, "year":year, "q_start":q_start, "q_end":q_end}
     # for year in range(1998,2009):
      #         for quarter in ('q1', 'q2', 'q3', 'q4'):

     # month = 0
     #  if quarter == 'q1': 
     #      month = 3
     #  elif quarter == 'q2':
     #      month = 6
     #  elif quarter == 'q3':
     #      month = 9
     #  elif quarter == 'q4':
     #      month = 12