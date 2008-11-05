import unittest
from MSR.main.GnomeDataObject import GnomeDataObject 
from MSR.main.SVNParser import SVNParser
import exceptions
import datetime

class TestError(exceptions.Exception):
    pass

class ParseSVNTestCase(unittest.TestCase):
    """Tests to see whether the object is properly created """
    filename = None
    parser = None
        
    def setUp(self):
        self.filename = "sample-data/totem.xml"
        self.parser = SVNParser()
    
#    def testLoadFile(self):
#        """ test whether the file is loaded"""
#        filename = "sample-data/totem.xml"
#        parser = SVNParser()
#        parser.loadFile(filename)
    
    def testLoadXML(self):
        """ can it handle XML """ 
        self.parser.loadFile(self.filename)
       
    def testParseLine(self):
        self.parser.loadFile(self.filename)
        self.parser.parseLine()
        self.assertEquals(len(self.parser.getData()), 781) # 781 is number of events in test.xml

    def tearDown(self):
        pass#self.l.cleanup()
    
    
if __name__ == "__main__":
    unittest.main()

