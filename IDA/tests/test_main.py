import unittest
import IDA
import random

class IDATestCase(unittest.TestCase):
        
    def test_file_not_exist(self): 
        with self.assertRaises(FileNotFoundError):
            IDA.split("notafile.xyz", 10,4)
            
    def test_numFragments_error(self): 
        with self.assertRaises(ValueError): 
            IDA.split("testfile_short.txt", 0,0)
        
        with self.assertRaises(ValueError): 
            IDA.split("testfile_short.txt", 0, -1)
        
    def test_numToAssemble_error(self): 
        with self.assertRaises(ValueError): 
            IDA.split("testfile_short.txt", 10,15)  
        
    def test_short_file(self): 
        original_file=open("testfile_short.txt", "r").read()  
        fragments=IDA.split("testfile_short.txt", 10,5)
        test=True
        for count in range(100): 
            fragments_to_assemble = [fragments[i] for i in random.sample(range(10), 5)]
            output = IDA.assemble(fragments_to_assemble)
            if not output==original_file: 
                test=False
        self.assertEqual(test,True)
        
    def test_long_file(self):     
        original_file=open("testfile_long.txt", "r").read()  
        fragments=IDA.split("testfile_long.txt", 100,75)
        test=True
        for count in range(100): 
            fragments_to_assemble = [fragments[i] for i in random.sample(range(100), 75)]
            output = IDA.assemble(fragments_to_assemble)
            if not output==original_file: 
                test=False
        self.assertEqual(test,True)
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(IDATestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
