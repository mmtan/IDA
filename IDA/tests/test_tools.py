import unittest
import numpy as np
import random
from IDA.tools import isPrime, nextPrime, inner_product, matrix_product, transpose, modulo_inverse, vandermonde_inverse


class IDAToolsTestCase(unittest.TestCase):
        
    def test_isPrime(self):
        test=True
        for p in [3,5,7,11,13,17,19,23,29,31]:
            if not isPrime(p): 
                test=False
                break
        self.assertEqual(test,True)
        
        for p in [12,16,33,49,29*3, 31*29]:
            if isPrime(p): 
                test=False
                break
        self.assertEqual(test,True)
    
    def test_nextPrime(self): 
        test=True
        for i in range(2,100): 
            p=nextPrime(i)
            if not isPrime(p): 
                test=False
                break
        self.assertEqual(test,True)
    
    def test_inner_product(self): 
        test=inner_product(list(range(100)), list(range(100)),257)
        self.assertEqual(test, np.dot(np.array(range(100)), np.array(range(100)))%257)
            
    def test_matrix_product(self): 
        
        I=np.identity(10).tolist()
        A=[random.sample(range(100), 10) for _ in range(10)]
        self.assertEqual(matrix_product(A,I,257),A)
        self.assertEqual(matrix_product(I,A,257),A)
        
        B=[random.sample(range(100), 10) for _ in range(10)]
        test=matrix_product(A,B,257)
        self.assertEqual(test,(np.matmul(np.array(A), np.array(B))%257).tolist())
        
    def test_transpose(self): 
        A=[random.sample(range(100), 10) for _ in range(10)]
        self.assertEqual(transpose(A), np.array(A).transpose().tolist())

    def test_modulo_inverse(self): 
        test=True
        for i in range(1,257): 
            if( modulo_inverse(i,257)*i)%257!= 1: 
                print(i)
                test=False
                break 
        self.assertEqual(test,True)
        
    def test_vandermonde_inverse(self): 
        basis=random.sample(range(1,257),125)
        p=257
        matrix=[[(x**j)%p for j in range(len(basis))] for x in basis]
        inverse=vandermonde_inverse(basis, p)
        test=np.matmul(np.array(matrix), np.array(inverse))
        test%=p
        self.assertEqual(test.tolist(), np.identity(len(basis)).tolist())

if __name__ == '__main__':
    unittest.main()
