import unittest, exceptions, random
#from MSR.main.GnomeDataObject import GnomeDataObject 
from MSR.main.SVNParser import SVNParser

class TestError(exceptions.Exception):
    pass

class ParseSVNTestCase(unittest.TestCase):
    """Tests to see whether the object is properly created """
    filename = "sample-data/totem.xml"
    parser = None
        
    def setUp(self):
        pass
        
    def testLoadXML(self):
        """ can it handle XML """ 
        parser = SVNParser()
        parser.load_file(self.filename)
       
    def testParseLine(self):
        """ test a variety of parsing and storing."""
        parser = SVNParser()
        parser.load_file(self.filename)
        parser.parse_line()
        self.assertEquals(len(parser.get_data()), 781) # 781 is number of events in test.xml
        
    def testObjectStore(self):
        """ test that the data object has valid information"""
        p = SVNParser()
        print len(p.get_data())
        p.load_file(self.filename)
        p.parse_line()
        data = p.get_data()
        print len(data)
        obj = random.choice(data) # a random obj
        self.failUnless(obj.getDate().year > 1992 and obj.getDate().year < 2010) # must be a sensible year 

    def tearDown(self):
        pass#self.l.cleanup()
    
    
if __name__ == "__main__":
    unittest.main()

