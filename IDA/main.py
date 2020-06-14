from IDA.tools import *
from IDA.fragment import *

        
def split(file, n, m): 
    """
    Inputs:
    file: name of the file to split
    n   : number of fragments after splitting the file
    m   : minimum number of fragments required to restore the file
    Output:
    a list of n fragments (as Fragment objects)
    """

    if m>n: 
        raise ValueError("numToAssemble must be less than numFragments")
        
    if n<=0 or m<=0: 
        raise ValueError("parameters numFragments and numToAssemble must be positive ingeters")
        
    # convert file to byte strings
    original_file=open(file, "rb").read()  
    
    # find the prime number greater than n
    # all computations are done modulo p
    p = 1021 if n<1021 else nextPrime(n)
    
    # split original_file into chunks (subfiles) of length m 
    original_subfiles=[list(original_file[i:i+m]) for i in range(0,len(original_file),m)]
    
    # for the last subfile, if the length is less than m, pad the subfile with zeros 
    # to achieve final length of m
    residue = len(original_file)%m
    if residue:
        
        last_subfile=original_subfiles[-1]
        last_subfile.extend([0]*(m-residue))
    

    building_blocks=[]
    for a in range(1,n+1): 
        row = []
        elt = 1
        for i in range(m): 
            row.append(elt)
            elt=(elt*a)%p
        building_blocks.append(row)
    
    fragments=[]
    for i in range(n): 
        fragment = []
        for k in range(len(original_subfiles)): 
            fragment.append(inner_product(building_blocks[i], original_subfiles[k],p))
        fragments.append(Fragment(i+1,fragment, n, m,p))
    
    return fragments

def assemble(fragments, filename=None): 
    '''
    Input: 
    fragments : a list of Fragments objects
    filename: a String for the name of the file to write
    Output: 
    String represents the content of the original file
    If filename is given, the content is written to the file
    '''
    
    
    n, m, p  = fragments[0].getNumFragments(), fragments[0].getNumAssemble(), fragments[0].getPrime()
    if len(fragments)<m:
        raise ValueError("Number of fragments is below the minimum number of fragments required to assemble the file.")
        
    # take the first m fragments
    fragments=fragments[:m]
    building_basis = [fragment.getIndex() for fragment in fragments]
    
    inverse_building_matrix = vandermonde_inverse(building_basis,p)
    fragments_matrix = [fragment.getContent() for fragment in fragments]
    output_matrix = matrix_product(inverse_building_matrix, fragments_matrix,p)
    
    # each column of output matrix is a chunk of the original matrix
    original_subfiles=[]
    ncol = len(output_matrix[0])
    nrow = len(output_matrix)
    for c in range(ncol): 
        col = [output_matrix[r][c] for r in range(nrow)]
        original_subfiles.append(col)
    
    # remove tailing zeros in the last chunk of the original file
    last_file = original_subfiles[-1]
    i=len(last_file)-1
    while i>=0 and last_file[i]==0: 
        i-=1
    original_subfiles[-1]=last_file[:i+1]
    
    # combine the original_subfiles
    original_file=[]
    for subfile in original_subfiles: 
        original_file.extend(subfile)
    
    
    # convert original_file to its content
    original_file_content = "".join(list(map(chr, original_file)))
    
    # write the output to file
    if filename:
        open(filename, "wb").write(bytes(original_file)) 
    
    return original_file_content
