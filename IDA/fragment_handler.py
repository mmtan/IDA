class ContentError(Exception): 
    pass
    
def fragment_writer(filename, original_file, fragments):

    # hash value of the original_file is used to check 
    # if the input "fragments_filenames" to the function "assemble" 
    # are derived from the same file
    original_file_hash = hash(original_file)
    
    # write fragments to files  
    # fragment i is written to the file <original_filename><original_file_hash>_i
    original_filename = filename.split(".")[0]
    fragment_filehandles={}    
    fragment_filenames=[]
    for idx in range(n): 
        fragment_filename = "{}_fragment{}".format(original_filename,idx )
        fragment_filenames.append(fragment_filename)
        fragment_filehandle = open(fragment_filename,'w')
        fragment_filehandles[idx]=fragment_filehandle
        fragment_content = str(fragments[idx])
        # compute the hash of hash(hash(fragment_content)+hash(original_file)) for error detection
        fragment_hash = hash(hash(fragment_content)+original_file_hash)
        # write identifiers for each file (idx,m,n,p,original_file_hash)
        fragment_filehandle.write("{} {} {} {} {} {}\n".format(idx, m, n, p,original_file_hash, fragment_hash))
        fragment_filehandle.write(fragment_content)
        fragment_filehandle.close()
    return fragment_filenames
    
def fragment_reader(filenames): 
    """
    Inputs: 
    filenames: a list of strings correspond to filenames of fragments
    Output:
    (m_, n_, p_, fragments): (int, int, int, [(idx, [int])]
    """
    fragments=[] 
    
    if not filenames: 
        return fragments
    
    # take the parameters m, n, p, original_file_hash of the first fragment
    # the rest of the fragments should have the same values for these parameters
    filename=filenames[0]
    with open(filename,'r') as fh:
        idx, m_, n_, p_, original_file_hash_, hashid_= map(eval,fh.readline().split(" "))

    # there should be at least m_ fragments
    if len(filenames)<m_:
        raise ValueError("Number of fragments is below the minimum number of fragments required to assemble the file.")
    
    # take the first m_ different fragments
    indices=set() # store the indices of the fragments
    count=0
    for filename in filenames:
        if count<m_:
            with open(filename,'r') as fh:
                
                idx, m, n, p, original_file_hash, hashid =map(eval,fh.readline().split(" "))
                
                # if idx is already in indices, skip this file
                if idx in indices: 
                    continue
                else: 
                    indices.add(idx)
                
                # check if the fragments have the same values of the parameters m, n, p, original_file_hash
                if (m,n,p,original_file_hash)!=(m_, n_,p_, original_file_hash_):
                    raise ValueError("These fragments are not derived from the same file.")
                content = fh.read()

                # check if the file content is corrupted
                if hash(hash(content)+original_file_hash)!=hashid:
                    raise ContentError("The content of {} has been compromised.".format(filename))

            fragments.append((idx+1,eval(content)))
            count+=1
        else: 
            break
    if count<m: 
        raise ValueError("There are duplicate fragments. The total number of different fragments are insufficient to assemble the file.")
    
    return (m_, n_, p_, fragments)
