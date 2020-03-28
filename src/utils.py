import os
import os.path as path
import ast

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
    parsed = { 'description' : '', 'params' : {}, 'throws' : {}, 'return' : [] }
    lines = docstring.splitlines()
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith('@param'):
            parts = line.split(maxsplit=2)
            if len(parts) < 3:
                raise Exception("Error parsing docstring for {} at {}".format(context, line))
            parsed['params'][parts[1]] = parts[2]
        elif line.startswith('@return'):
            parts = line.split(maxsplit=1)
            if len(parts) < 2:
                raise Exception("Error parseing docstring for {} at {}"
                    .format(context, line))
            parsed['return'].append( parts[1] )
        elif line.startswith('@throws'):
            parts = line.split(maxsplit=2)
            if len(parts) < 3:
                raise Exception("Error parsing docstring for {} at {}"
                    .format(context, line))
            parsed['throws'][parts[1]] = parts[2]
        else:
            parsed['description'] += line + ' '
    return parsed


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
