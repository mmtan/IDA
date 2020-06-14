class Fragment: 
    def __init__(self, idx, content, n,m,p): 
        self.idx=idx
        self.content=content # the encoded content of the fragment
        self.numFragments=n # number of fragments from the original message
        self.numToAssemble=m # number of fragments required for reconstruction
        self.prime=p
        
    def getIndex(self): 
        return self.idx
    
    def getContent(self): 
        return self.content
    
    def getNumFragments(self): 
        return self.numFragments
    
    def getNumAssemble(self): 
        return self.numToAssemble
    
    def getPrime(self): 
        return self.prime
    
    def __repr__(self): 
        return "{}:{}".format(self.idx,self.content)
