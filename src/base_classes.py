# base classes
import datetime
import re

class Parser(object):
    """this is an abstract parser object - it loads a text file
    parses the line and stores the tokens somehow"""
    
    STORAGE_TABLE = "t_data"
    STORAGE_DB = "data_objects"

    def load_file(self, filename):
        pass
    
    def parse_line(self):
        pass
    
    def store_tokens(self, node):
        pass
    
    def __init__(self):
        pass
        
# created by the parser 


class GnomeDataObject():
    """ Data structure for storing in MySQL (define ORM?)"""
    
    date = None # a Python datetime.Date object
    event = None # the text associated with some change to the product e.g. mail, changelog, commit comment, bug report
    rsn = None # the release sequence number, e.g. the changeset. -1 indicates no RSN
    eventtype = None # one of SVN, BUG, CHANGE, MAIL
    SVN = "SVN"
    BUG = "Bug"
    CHANGE = "Changelog"
    MAIL  = "Mail"
    
    def __init__(self,eventtype):
        self.eventtype = eventtype    
        
    def setDate(self, date):
        self.date = date
        
    def getDate(self):
        ''' return a date formatted as an ISO string'''
        if self.date != None:
            return self.date.isoformat()
        else:
            return "no date" # a nothing date
    
    def getEvent(self):
        if self.event != None:
            return self.event
        else:
            return "no event" # a nothing event    
        
    def setEvent(self, event):
        self.event = event
        
    def getType(self):
        if self.eventtype != None:
            return self.eventtype
        else:
            return "no type" # a nothing type
        
    def getRSN(self):
        if self.rsn != None:
            return self.rsn
        else:
            return -1 # a nothing rsn
        
    def setRSN(self, rsn):
        self.rsn = rsn
        
    def __str__(self):
        return "type: " + self.getType() + " date: "+  self.getDate() + \
                " RSN: " + str(self.getRSN()) + " Event: " + self.getEvent()