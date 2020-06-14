# IDA

This is a Python library for the implementation of the Information Dispersal Algorithm (IDA) introduced in [1].
IDA is developed to break a file F of length N into n fragments, each of length N/m such that any m such fragments can recover the original file F. 
The parameters n and m can be chosen to be close to 1, hence, IDA is space efficient. 
Splitting and reconstruction of a file is computationally efficient. 
The reader may refer to  [1] for the many applications of IDA, including the use of IDA for routing of data in parallel computers. 


[1] Rabin, Michael O. "Efficient dispersal of information for security, load balancing, and fault tolerance." Journal of the ACM (JACM) 36.2 (1989): 335-348.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install IDA.

```bash
pip install IDA-pkg
```

## Examples
The following is a simple example. That is, we split a file into 10 fragments such that any 5 of them are sufficient to recover the original data. 

```python
import IDA
fragments = IDA.split("test.txt", 10, 5) 
```

To reassemble the file, we take a minimum 5 of the fragments, e.g., we take the first five fragments, then the following will return the content of the original file as a string. 

```python
import IDA
IDA.assemble(fragments[:5]) 
```

The user can also write the output to a file. 
```python
import IDA
IDA.assemble(fragments[:5], "output.txt") 
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Future work
* Encrypt fragments for secret sharing. 
* Optimize splitting process for large input files.

## License
[MIT](https://choosealicense.com/licenses/mit/)
