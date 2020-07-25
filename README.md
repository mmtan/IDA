# IDA

This library implements the Information Dispersal Algorithm (IDA) introduced in [1].
IDA breaks up a file of size N into n fragments, each of size N/m such that the original file can be recovered from any m of these fragments.
Note that after IDA splits the file, the total size of all the fragments is(n/m)N. 
The parameters n and m can be chosen such that their ratio is close to 1, and hence, the total size of all the fragments after splitting the original file is close to the size of the original file, making IDA space-efficient. 

[1] Rabin, Michael O. "Efficient dispersal of information for security, load balancing, and fault tolerance." Journal of the ACM (JACM) 36.2 (1989): 335-348.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install IDA.

```
pip install IDA-pkg
```

<!-- ## Issues -->
<!-- * Warning: currently only works with small files! -->

## Examples
The following is a simple example. That is, we split a file into 10 fragments such that any 5 of them are sufficient to recover the original data. 

```python
import IDA
IDA.split("test.txt", 10, 5) 
```

Alternatively, we can execute the command in the command line interface as follows. 

```
IDAsplit "test.txt" 10 5
```

The following ten files (call fragments) will be generated: 
"test_fragment0"
"test_fragment1"
"test_fragment2"
"test_fragment3"
...
"test_fragment9"

To reassemble the file "test.txt", we take any 5 of the fragments, e.g., we take the first five fragments, then the following will return the content of the original file as a string. 

```python
import IDA
IDA.assemble(["test_fragment0", "test_fragment1", "test_fragment2", "test_fragment3", "test_fragment4"]) 
```

You can also write the output to a file. 

```python
IDA.assemble(["test_fragment0", "test_fragment1", "test_fragment2", "test_fragment3", "test_fragment4"], "output.txt") 
```

Alternatively, we can execute the command in the command line interface as follows. 

```
IDAassemble "test_fragment0" "test_fragment1" "test_fragment2" "test_fragment3" "test_fragment4"
```

```
IDAassemble "test_fragment0" "test_fragment1" "test_fragment2" "test_fragment3" "test_fragment4" -write "output.txt"
```

## Supported features
* Detect if all the fragment files for assembling are derived from the same original file. 
* Detect if a fragment file is corrupted before assembling. 
  - Error detection is realized by adding the output of the application of hash function SHA-224 on the content of the file ( such output is called message digest) to the file. The hash value of the content of the file is recomputed in the IDA.assemble function and is compared with the message digest tagged in the file. Error detection using SHA-224 provides 112 bits of security againts collision attacks. 


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License
[MIT](https://choosealicense.com/licenses/mit/)
