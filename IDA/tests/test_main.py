import unittest
import IDA
import random

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
            IDA.split("testfile_short.txt", 0,0)
            
        # numFragments<numToAssemble
        with self.assertRaises(ValueError): 
            IDA.split("testfile_short.txt", 10,15)
            
        # numFragments is negative      
        with self.assertRaises(ValueError): 
            IDA.split("testfile_short.txt", -1, -2)
   
    def test_numToAssemble_error(self):
        files=IDA.split("testfile_short.txt", 10,5)
        
        # insufficient numToAssemble
        with self.assertRaises(ValueError): 
            IDA.assemble(files[:4])
            
        # insufficient distinct numToAssemble
        with self.assertRaises(ValueError): 
            IDA.assemble([files[i] for i in [2,4,6,8,2]])
            
    def test_fragments_error(self): 
        files1=IDA.split("testfile_short.txt", 10,5)
        files2=IDA.split("testfile_long.txt", 10,5)
        
        
        # files to assembled are not derived from the same file
        with self.assertRaises(ValueError): 
            IDA.assemble(files1[:4]+[files2[0]])
            
        # files to assembled are compromised
        # the file "IDA/tests/testfile_short_fragment0_compromised" is a compromised version 
        # the file "IDA/tests/testfile_short_fragment0"
        with open("testfile_short_fragment0", "r") as fh:
            parameters=fh.readline()
            file_hash=fh.readline()
            content_hash=fh.readline()
            fragment=eval(fh.readline())
        fragment[-1]+=1
        with open("testfile_short_fragment0_compromised", "w") as fh:
            fh.write(parameters)
            fh.write(file_hash)
            fh.write(content_hash)
            fh.write(str(fragment))
        with self.assertRaises(IDA.fragment_handler.ContentError): 
            IDA.assemble(files1[1:5]+["testfile_short_fragment0_compromised"])
        
        files3=IDA.split("testfile_short.txt", 10,6)
         # files to assembled are not output of the same split function with parameters
        with self.assertRaises(ValueError): 
            IDA.assemble(files1[:4]+[files3[0]])
            

    def test_short_file(self): 
        original_file=open("testfile_short.txt", "rb").read()  
        fragments=IDA.split("testfile_short.txt", 10,5)
        original_file_hash=hash(original_file)
        test=True
        for count in range(100): 
            fragments_to_assemble = [fragments[i] for i in random.sample(range(10), 5)]
            output = IDA.assemble(fragments_to_assemble)
            if not (original_file==bytes(output,encoding='utf8')):
                test=False
                break
        self.assertEqual(test,True)
        
    def test_long_file(self):     
        original_file=open("testfile_long.txt", "rb").read()  
        original_file_hash=hash(original_file)
        fragments=IDA.split("testfile_long.txt", 100,75)
        test=True
        for count in range(100): 
            fragments_to_assemble = [fragments[i] for i in random.sample(range(100), 75)]
            output = IDA.assemble(fragments_to_assemble)
            if not (original_file==bytes(output,encoding='utf8')):
                test=False
                break
        self.assertEqual(test,True)        

if __name__ == '__main__':
    unittest.main()
