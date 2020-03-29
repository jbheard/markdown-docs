import os
import os.path as path
import ast
from tag import Tag


def get_all_files(dir, extension):
    """
    Gets all files with a given extension under a directory
    Checks subfolders as well as top-level
    @param dir directory to search in
    @param extension file extension to check for
    @return a list of filenames (strings)
    """
    filenames = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            if name.endswith(extension):
                filenames.append( path.join(root, name) )
    return filenames

def load_ast(filename):
    """
    loads an ast from a python file
    @param filename the name of the file to load
    @return an ast loaded from the file
    """
    with open(filename, 'r') as f:
        return ast.parse(f.read())

def get_classes(_ast):
    """
    Gets all function definitions immediately below an ast node
    @param _ast the ast node to search for functions in
    @return a tuple of class definition ast nodes
    """
    return (node for node in _ast.body if isinstance(node, ast.ClassDef))

def get_functions(_ast):
    """
    Gets all function definitions immediately below an ast node
    @param _ast the ast node to search for functions in
    @return a tuple of function definition ast nodes
    """
    return (node for node in _ast.body if isinstance(node, ast.FunctionDef))

def parse_docstring(docstring, context):
    """
    Parses parameters, thrown exception types, return values, 
    and description from the docstring
    @param docstring the docstring to parse data from
    @param context the function or class that the docstring belongs to, used for errors
    @return a dict with keys 'params', 'description', 'throws', and 'return'
    """
    parsed = { 'description' : '' }
    lines = docstring.splitlines()
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith('@'):
            collection, result = Tag.parse(line)
            if collection not in parsed:
                parsed[collection] = []
            parsed[collection].append(result)
        else:
            parsed['description'] += line + ' '
    return parsed

def template_to_file(template, data, out_path):
    """
    write a rendered template to a file
    @param template the jinja2 template to use
    @data the dict object to put through the template
    @out_path the output file path
    """
    with open(out_path, 'w') as f:
        f.write( template.render(data) )

# TODO: maybe use a library to convert the ast to a string?
# In particular, the lambda doesn't give very meaningful information here
def ast_object_to_str(ast_obj):
    if isinstance(ast_obj, ast.Num):
        return str(ast_obj.n)
    if isinstance(ast_obj, ast.Lambda):
        return 'lambda ' + ','.join( arg.arg for arg in ast_obj.args.args )
    if isinstance(ast_obj, ast.NameConstant):
        return str(ast_obj.value)
    if isinstance(ast_obj, ast.Str):
        return '"' + str(ast_obj.s) + '"'
    return ''
