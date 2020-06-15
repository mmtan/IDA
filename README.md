# IDA

This is a library that implements the Information Dispersal Algorithm (IDA) introduced in [1].
IDA breaks up a file of size N into n fragments, each of size N/m such that the original file can be recovered from any m of these fragments.
Note that after IDA splits the file, the total size of all the fragments is(n/m)N. 
The parameters n and m can be chosen such that their ratio is close to 1, and hence, the total size of all the fragments after splitting the original file is close to the size of the original file, making IDA space-efficient. 

[1] Rabin, Michael O. "Efficient dispersal of information for security, load balancing, and fault tolerance." Journal of the ACM (JACM) 36.2 (1989): 335-348.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install IDA.

```
pip install IDA-pkg
```

## Issues
* Warning: currently only works with small files!

## Examples
The following is a simple example. That is, we split a file into 10 fragments such that any 5 of them are sufficient to recover the original data. 

```python
import IDA
fragments = IDA.split("test.txt", 10, 5) 
```

To reassemble the file, we take any 5 of the fragments, e.g., we take the first five fragments, then the following will return the content of the original file as a string. 

```python
import IDA
IDA.assemble(fragments[:5]) 
```

You can also write the output to a file. 

```python
IDA.assemble(fragments[:5], "output.txt") 
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License
[MIT](https://choosealicense.com/licenses/mit/)
