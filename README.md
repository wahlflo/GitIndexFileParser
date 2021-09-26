# GitIndexFileParser

A package to parse the index file of a git repository.

## Installation

Install the package with pip

    pip install git_index_parser


## Usage
```
from git_index_parser import GitIndexParser

index_file = GitIndexParser.parse_file(path_to_file='.git/index')

for entry in index_file.get_entries():
    print(entry.name.split)
```