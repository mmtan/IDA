import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="IDA-pkg", 
    version="0.0.1",
    author="mmtan",
    author_email="mmtan830@gmail.com",
    description="Python package for efficient dispersal of information that breaks a file of length N into n pieces, each of length N/m, so that every m pieces are sufficient to reconstruct the original file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
