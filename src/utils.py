import os, sys, ast
from jinja2 import Template
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
                filenames.append( os.path.join(root, name) )
    return filenames

def load_template(template_path, static=False):
    """
    Load a jinja2 template from a file
    @param template_path the path to load the file from
    @param static True to load the templates from the application path, False to load normally
    @return a jinja2 template
    """
    if static:
        root = os.path.dirname(sys.argv[0])
        template_path = os.path.join(root, template_path)
    with open(template_path, 'r') as f:
        template = Template(f.read())
    return template

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
    @return a dict with keys from docstring tags
    """
    parsed = { 'description' : '' }
    lines = docstring.splitlines()
    i = 0
    while i < len(lines) and not lines[i].startswith('@'):
        if len(lines[i]) == 0:
            parsed['description'] += '  \n'
        else:
            parsed['description'] += lines[i].strip() + ' '
        i += 1
    curr = ''
    for line in lines[i:]:
        line = line.strip()
        if len(line) == 0: continue

        if line.startswith('@'):
            if curr != '':
                collection, result = Tag.parse(curr)
                if result is not None:
                    if collection not in parsed:
                        parsed[collection] = []
                    parsed[collection].append(result)
            curr = line
        else:
            curr += ' ' + line
    if curr != '':
        collection, result = Tag.parse(curr)
        if result is not None:
            if collection not in parsed:
                parsed[collection] = []
            parsed[collection].append(result)
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
