# created by the parser 
import datetime

class GnomeDataObject():
    
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
        if self.date != None:
            return self.date.isoformat()
        else:
            return "no date" # a nothing date
    
    def getEvent(self):
        if self.event != None:
            return self.event
        else:
            return "no event" # a nothing date    
        
    def setEvent(self, event):
        self.event = event
        
    def getType(self):
        if self.eventtype != None:
            return self.eventtype
        else:
            return "no type" # a nothing date
        
    def getRSN(self):
        if self.rsn != None:
            return self.rsn
        else:
            return -1 # a nothing date
        
    def setRSN(self, rsn):
        self.rsn = rsn
        
    def __str__(self):
        return "type: " + self.getType() + " date: "+  self.getDate() + " RSN: " + str(self.getRSN()) + " Event: " + self.getEvent()