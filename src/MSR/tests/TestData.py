import unittest
from MSR.main.GnomeDataObject import GnomeDataObject 
import exceptions
import datetime

class TestError(exceptions.Exception):
    pass

class loadFileTestCase(unittest.TestCase):
    """Tests to see whether the object is properly created """
        
    def setUp(self):
        pass
    
    def testCreate(self):
        """ test whether the object was properly created"""
        gdo = GnomeDataObject()
       
    def testGetDate(self):
        """ test whether date is in the right format"""
        date = datetime.datetime(1999, 8, 24, 18, 30, 22)
        gdo = GnomeDataObject()
        gdo.setDate(date)
        self.assertTrue(gdo.getDate() == datetime.datetime(1999, 8, 24, 18, 30, 22 ))
        
    def testGetEvent(self):
        """ test whether the event is returned """
        event =  """
         I says to him, Evan I sez, what in Heaven are ya doin' boyo!?
         Heavens to Betsy, man. Get that cod back in da Sea!
         """
        gdo = GnomeDataObject()
        gdo.setEvent(event)
        self.assertTrue(event == gdo.getEvent())
               
def tearDown(self):
        pass#self.l.cleanup()
    
    
if __name__ == "__main__":
    unittest.main()

