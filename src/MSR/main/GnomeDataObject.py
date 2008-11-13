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
        return self.date
    
    def getEvent(self):
        return self.event
    
    def setEvent(self, event):
        self.event = event
        
    def getType(self):
        return self.eventtype
    
    def getRSN(self):
        return self.rsn
    
    def setRSN(self, rsn):
        self.rsn = rsn
        
    def __str__(self):
        return "type: " + self.getType() + " date: "+  self.getDate().isoformat() + " RSN: " + str(self.getRSN()) + " Event: " + self.getEvent()