import unittest
import IDA
import random

class IDATestCase(unittest.TestCase):
        
    def test_file_not_exist(self): 
        with self.assertRaises(FileNotFoundError):
            IDA.split("notafile.xyz", 10,4)
            
    def test_numFragments_error(self): 
        # numFragments is zero
        with self.assertRaises(ValueError): 
            IDA.split("IDA/tests/testfile_short.txt", 0,0)
            
        # numFragments<numToAssemble
        with self.assertRaises(ValueError): 
            IDA.split("IDA/tests/testfile_short.txt", 10,15)
            
        # numFragments is negative      
        with self.assertRaises(ValueError): 
            IDA.split("IDA/tests/testfile_short.txt", -1, -2)
   
    def test_numToAssemble_error(self):
        files=IDA.split("IDA/tests/testfile_short.txt", 5,10)
        
        # insufficient numToAssemble
        with self.assertRaises(ValueError): 
            IDA.assemble(files[:4])
            
        # insufficient distinct numToAssemble
        with self.assertRaises(ValueError): 
            IDA.assemble([files[i] for i in [2,4,6,8,2]])
            
    def test_fragments_error(self): 
        files1=IDA.split("IDA/tests/testfile_short.txt", 10,5)
        files2=IDA.split("IDA/tests/testile_long.txt", 10,5)
        files3=IDA.split("IDA/tests/testfile_short.txt", 10,6)
        
        # files to assembled are not derived from the same file
        with self.assertRaises(ValueError): 
            IDA.assemble(files1[:4]+files2[0])
            
        # files to assembled are not output of the same split function with parameters
        with self.assertRaises(ValueError): 
            IDA.assemble(files1[:4]+files3[0])
        
        # files to assembled are compromised
        file=files1[0]
        with open(file,'a') as fh:
            fh.write("\nThis is a line that is not suppose to be here.\n")
        with self.assertRaises(ContentError): 
            IDA.assemble(files1[:5])
        
        
    def test_short_file(self): 
        original_file=open("IDA/tests/testfile_short.txt", "r").read()  
        fragments=IDA.split("IDA/tests/testfile_short.txt", 10,5)
        original_file_hash=hash(original_file)
        test=True
        for count in range(100): 
            fragments_to_assemble = [fragments[i] for i in random.sample(range(10), 5)]
            output = IDA.assemble(fragments_to_assemble)
            if not hash(output)==original_file_hash:
                test=False
            else: 
                test=original_file==output
        self.assertEqual(test,True)
        
    def test_long_file(self):     
        original_file=open("IDA/tests/testfile_long.pdf", "r").read()  
        original_file_hash=hash(original_file)
        fragments=IDA.split("IDA/tests/testfile_long.pdf", 100,75)
        test=True
        for count in range(100): 
            fragments_to_assemble = [fragments[i] for i in random.sample(range(100), 75)]
            output = IDA.assemble(fragments_to_assemble)
            if not hash(output)==original_file_hash:
                test=False
            else: 
                test=original_file==output
        self.assertEqual(test,True)
        a
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(IDATestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
