# created by the parser 
import datetime

class GnomeDataObject():
    
    date = None
    event = None
    
    def setDate(self, date):
        self.date = date
        
    def getDate(self):
        return self.date
    
    def getEvent(self):
        """ event is a simple string that details what happened at time <date> e.g., commit, mail message, code comment... """
        return self.event
    
    def setEvent(self, event):
        self.event = event