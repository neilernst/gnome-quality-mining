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
The help message goes here.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def connect_corpus(db_name):
    """ connect to db"""
    self.storedb = MySQLdb.connect(passwd="hello", db=db_name, cursorclass=DictCursor)
    self.store_cursor = self.storedb.cursor()
    
def get_counts(self, keyword, product, quarter, year):
    """ store in the database"""
    store_con = connect_corpus("data_objects")
    query_string = """select count(*) from t_data where match(event) against (%s in boolean mode) \
                    and product = %s and  msr_date \
                    between cast('%s-07-01' as Datetime) and cast('%s-09-30' as Datetime)""" % (keyword, product, year, year)
    try:
        store_cursor.execute(query_string)
    except (ValueError):
        print 'Error in query syntax'

def main(argv=None):
    product = ''
    keyword = ''
    
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
    get_counts(keyword, product, 'q1', 2003)
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
