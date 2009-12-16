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
    db_name = 'data_objects'#'msr_data'
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
    return normalize(result, total)

def normalize(result, total):
    """Takes a dictionary with absolute counts and a dictionary with message frequency.
    Returns a tuple with the dateweek, absolute value, and normalized value"""
    normal_multiplier = 1000 #set appropriately to get results between 0 and 1000
    #Mysql yearweek() function has default mode of 0, weeks start Sunday and week 1 is first week with sunday in the year.
    complete_year_weeks = []
    years = [199800,199900,200000,200100,200200,200300,200400,200500,200600,200700,200800]
    weeks = [i for i in range(0,54)]
    for y in years:
        for w in weeks:
             complete_year_weeks.append(y+w)
     
    result_dict = {}
    for r in result:
         k = r.keys()
         v = r.values()
         if k[0] in result_dict.keys():
            result_dict[k[0]] = result_dict[k[0]] + v[0] #previous value
            #print str(k[0]) + ' was a dupe'
         else:        
             result_dict[k[0]] = v[0]
     
    total_dict = {}
    for t in total:
         k = t.keys()
         v = t.values()
         if k[0] in total_dict.keys():
              total_dict[k[0]] = total_dict[k[0]] + v[0] #previous value
              #print str(k[0]) + ' was a dupe'
         else:
              total_dict[k[0]] = v[0]
         
    # for each element in total
    result_lst = []
    save = False # determine if there is *any* data to save
    for c in complete_year_weeks:
        try:
            res_value = result_dict[c]  # find that year week in result
            save = True #omit leading zero results
        except(KeyError):
            res_value = 0
        try:
            total_value = total_dict[c] 
        except(KeyError):
            total_value = 0 #there was no value for that year
        normal = 0.0
        if total_value != 0:
            normal = normal_multiplier*float(res_value)/float(total_value)        
        res_tuple = (c, normal, res_value) # e.g., (200803, 3.3, 55)
        if save:
            result_lst.append(res_tuple)
    return result_lst
         
def save_file(result, product, signified):
    mac_loc = '/Users/nernst/Documents/current-papers/icsm09/data/pickles/'
    comps_loc = '/u/nernst/msr/data/icsm-pickles2/'
    f = file(comp_loc+product+'-'+ signified + '.pcl', 'wb')
    import pickle
    pickle.dump(result, f)
    f.close()
    
def main():
    t = Taxonomy()     
    #result = query_database('Evolution', t.get_signifiers('Usability'))
    for signified in t.get_signified(): # e.g. usability, performance, etc
        for product in t.get_products():
            result = query_database(product, t.get_signifiers(signified)) #e.g. usability: usability, usable, etc.
            save_file(result, product, signified)
    
if __name__ == "__main__":
    sys.exit(main())
