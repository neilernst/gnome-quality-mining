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

    query_string = """select count(*) from data where match(event) against (\'%(key)s\' in boolean mode) and 
                        product = \'%(product)s\' and  msr_date between cast(\'%(year)s-%(q_end)s\' as Datetime) and 
                        cast(\'%(year)s-%(q_start)s\' as Datetime)""" % {"key":keyword, "product":product, "year":year, "q_start":q_start, "q_end":q_end}

    #print  query_string
    try:
        pass
        store_cursor.execute(query_string)
        return str(store_cursor.fetchone().values()[0]) #{'count(*)': 6L} dict
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
        
        for year in range(1998,2009):
            result_lst = ()
            for quarter in ('q1', 'q2', 'q3', 'q4'):
                result = get_counts(keyword, product, quarter, year)
                result_lst
                #print str(year) + ' ' + quarter + ': ' + 
                print result_lst
                
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
#TODO divide by number of bugs per quarter (normalize?)
#TODO account for misspelinges 

class Taxonony():
    """ class to store lists of various terms of interest. Each element/term in the list will be queried once."""
    
    usability = ()