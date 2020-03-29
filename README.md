# Python Markdown Documentation Action

This action is meant to be a simple yet flexible way to convert python docstrings into markdown documentation.
Despite being made for markdown, it also support other formats. 

Markdown and HTML templates are provided, but custom templates can be used, as well as custom docstring tags.

## Using the action

This action can be easily added to your workflow, example working action:

```
name: Build Docs and Open PR
on:
  push:
    branches: [ master ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Generate Python Docs
      uses: jbheard/markdown-docs@v1
    - name: Open docs update PR
      uses: peter-evans/create-pull-request@v2
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
```

This uses the [create-pull-request](https://github.com/marketplace/actions/create-pull-request) action to open a pull request with the generated docs.

Note that input and output directories can be set with `src_path` and `dst_path` respectively. If not set, the action will look through your entire repo for python files to document, and will put the docs in `/docs`.

## Tags

Tags are defined in the yaml file `src/tags.yaml`, a tag is in the form `@mytag`, the default tags that are defined are below.

tag | decription | example
--- | --- | ---
@author | to add who authored the current piece of code | @author jbheard
@return | what the function returns | @return The list, but in reverse
@param | description of a parameter | @param the_list the list to be reversed
@throws | when different exceptions can expect to be thrown | @throws ValueError if a list contains non-numbers


These tags will always be loaded. Additional tags can be defined in a new yaml file in the following format:

```yaml
- syntax: @my_tag <list of operands>
  collection: collection_name
```

`syntax` defines the syntax to use for the tag, and each operand will be the name that the data is accessible under for templating. If syntax has a single operand, then it will be added to a 1D list. If there are multiple operands, they will be used as keys in a named collection.  
Example: `@my_tag op1 op2` will produce a list of `{'op1': value, 'op2': value}` objects. @throws and @param work this way, while @authors and @return are put into a 1D list.

`collection` tells the tag which collection to put the data in.

For examples, see [tags.yaml](src/tags.yaml). You can also take a look in [templates](/templates) to see how the tags are used.

### TODO Add command line argument to load tags from other yaml files


## Templates

Default templates are defined in `/templates`. 
The default templates used are readme.md and class.md, used to generate a readme and class files respectively. There is also an HTML option which uses index.html and class.html, and will also copy style.css into the output directory.

To define your own templates, provide 

### Template Variables

There are three different scopes of template object, global, class, and function.

There is a single global scoped object which is passed to the index template. It contains all of the documentation information and is formatted as:

```
title: title 
classes: list of class scoped objects
functions: list of all functions scoped objects not defined in a class
```

class scoped objects:
```
name: name of the class
href: link to the generated doc file for this class
description: description of the class
functions: list of function scoped objects defined in this class
```

function scoped objects:
```
name: name of the function
description: description of the function
params: list of arguments in the form 
        {name:argname, description: <...>, default: <defaultvalue or ''>}
```

function and class scoped objects parse data from the docstring as well as the code, so any tags defined in the docstring would appear in those objects as well.

For example, a function scoped object could look like:
```
name: reverse_list
description: reverses a list
return: ["The list, but in reverse"]
throws: [{"ValueError": "if a list contains non-numbers"}]
authors: ["jbheard"]
```
