from IDA.tools import *
from IDA.fragment import *
import os
import math
        
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
    
    # find the prime number greater than n
    # all computations are done modulo p
    p = 1021 if n<1021 else nextPrime(n)
    
    # row i of building_blocks is (1,a_i, a_i**2, ..., a_i**(m-1))
    building_blocks=[]
    for a in range(1,n+1): 
        row = []
        elt = 1
        for i in range(m): 
            row.append(elt)
            elt=(elt*a)%p
        building_blocks.append(row)
        
    # iteratively read segments of the file of size m
    # build fragments column by column
    # the entry of fragments at row i column j is the inner product of building_blocks[i] and 
    # j-th segment of the original file
    file_stats = os.stat(file)
    original_file_len = file_stats.st_size
    original_file=open(file, "rb")
    fragment_len = math.ceil(original_file_len/m)
    fragments_list=[[0]*fragment_len for _ in range(n)]
    
    original_subfile=original_file.read(m)
    col=0
    while original_subfile: 
        for row in range(n): 
            fragments_list[row][col]=inner_product(original_subfile, building_blocks[row],p)
        col+=1
        original_subfile=original_file.read(m)
    
    return [Fragment(idx+1,fragments_list[idx],n,m,p) for idx in range(n)]
    
        
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
