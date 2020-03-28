# Python Documentation

## Classes

**[Potato](Potato.md)**: This is the potato class, it is just to demonstrate the markdown abilities of this action. 



## Functions

### make_readme_md

#### Parameters
name | description | default
---|---|---
classes |  | 
functions |  | 


### make_class_md

#### Parameters
name | description | default
---|---|---
_class |  | 


### get_function_md

#### Parameters
name | description | default
---|---|---
func |  | 
context |  | <_ast.Str object at 0x00000229D7B3C0B8>


### get_all_files

Gets all files with a given extension under a directory Checks subfolders as well as top-level 

#### Parameters
name | description | default
---|---|---
dir | directory to search in | 
extension | file extension to check for | 


### load_ast

loads an ast from a python file 

#### Parameters
name | description | default
---|---|---
filename | the name of the file to load | 


### get_classes

Gets all function definitions immediately below an ast node 

#### Parameters
name | description | default
---|---|---
_ast | the ast node to search for functions in | 


### get_functions

Gets all function definitions immediately below an ast node 

#### Parameters
name | description | default
---|---|---
_ast | the ast node to search for functions in | 


### parse_docstring

Parses parameters, thrown exception types, return values, and description from the docstring 

#### Parameters
name | description | default
---|---|---
docstring | the docstring to parse data from | 
context | the function or class that the docstring belongs to, used for errors | 


