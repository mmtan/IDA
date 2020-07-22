from IDA.tools import build_building_blocks, inner_product, nextPrime
from IDA.fragment_handler import fragment_writer
import argparse

def split(filename, n, m): 
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
    p = 257 if n<257 else nextPrime(n)
    
    # convert file to byte strings
    original_file=open(filename, "rb").read()  
    
    # split original_file into chunks (subfiles) of length m 
    original_segments=[list(original_file[i:i+m]) for i in range(0,len(original_file),m)]
    
    # for the last subfile, if the length is less than m, pad the subfile with zeros 
    # to achieve final length of m
    residue = len(original_file)%m
    if residue:
        
        last_subfile=original_segments[-1]
        last_subfile.extend([0]*(m-residue))
    
    
    building_blocks=build_building_blocks(m,n,p)
    
    fragments=[]
    for i in range(n): 
        fragment = []
        for k in range(len(original_segments)): 
            fragment.append(inner_product(building_blocks[i], original_segments[k],p))
        fragments.append(fragment)
    
    return fragment_writer(filename, original_file, fragments)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split the file")
    parser.add_argument("filename", help="The file name.")
    parser.add_argument("numFragments", help = "Number of fragments after splitting the original file.")
    parser.add_argument("numToAssemble", help = "Minimum number of fragments required to assemble/restore the original file. ")
    args = parser.parse_args()
    main(args.filename, args.numFragments, args.numToAssemble)
