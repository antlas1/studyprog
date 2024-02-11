import unittest
from todo_core import add, rem, display
import todo_cli

curr_print = []
def print_fun(key,text):
    global curr_print
    curr_print.append((key,text))

class TestStringMethods(unittest.TestCase):

    def test_create(self):
        v = add(None,'First')
        self.assertTrue(isinstance(v,dict))
        keylist = list(v.keys())
        self.assertTrue(len(keylist)==1)
        self.assertTrue(keylist[0]==1)
        self.assertTrue(v[1]=='First')
        
    def test_add(self):
        v = add(None,'First')
        v = add(v,'Second')
        v = add(v,'Third')
        self.assertTrue(isinstance(v,dict))
        keylist = list(v.keys())
        self.assertTrue(len(keylist)==3)
        self.assertTrue(keylist[0]==1)
        self.assertTrue(keylist[1]==2)
        self.assertTrue(keylist[2]==3)
        self.assertTrue(v[1]=='First')
        self.assertTrue(v[2]=='Second')
        self.assertTrue(v[3]=='Third')
        
    def test_rem_ok(self):
        v = add(None,'First')
        v = add(v,'Second')
        v = add(v,'Third')
        v = rem(v,2)
        self.assertTrue(isinstance(v,dict))
        keylist = list(v.keys())
        self.assertTrue(len(keylist)==2)
        self.assertTrue(keylist[0]==1)
        self.assertTrue(keylist[1]==3)
        self.assertTrue(v[1]=='First')
        self.assertTrue(v[3]=='Third')
        
    def test_rem_fail(self):
        v = add(None,'First')
        v = add(v,'Second')
        v = add(v,'Third')
        v = rem(v,5)
        self.assertTrue(v==None)
        
    def test_display(self):
        v = add(None,'First')
        v = add(v,'Second')
        v = add(v,'Third')
        display(v,print_fun)

if __name__ == '__main__':
    unittest.main()