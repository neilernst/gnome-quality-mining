import unittest
from MSR.main.GnomeDataObject import GnomeDataObject 
from MSR.main.SVNParser import SVNParser
import exceptions
import datetime

class TestError(exceptions.Exception):
    pass

class ParseSVNTestCase(unittest.TestCase):
    """Tests to see whether the object is properly created """
        
    def setUp(self):
        pass
    
#    def testLoadFile(self):
#        """ test whether the file is loaded"""
#        filename = "sample-data/totem.xml"
#        parser = SVNParser()
#        parser.loadFile(filename)
    
    def testLoadXML(self):
        """ can it handle XML """ 
        filename = "sample-data/totem.xml"
        parser = SVNParser()
        parser.loadFile(filename)
       

    def tearDown(self):
        pass#self.l.cleanup()
    
    
if __name__ == "__main__":
    unittest.main()

