import os, sys, ast
from jinja2 import Template
from tag import Tag

from typing import Generator

def get_all_files(dir: str, extension: str) -> list[str]:
    """
    Gets all files with a given extension under a directory & subdirectories (case insensitive)
    @param dir directory to search
    @param extension file extension to find
    @return a list of filenames (strings)
    """
    extension = extension.lower()
    filenames = []
    for root, _, files in os.walk(dir):
        for name in files:
            if name.lower().endswith(extension):
                filenames.append( os.path.join(root, name) )
    return filenames

def load_template(template_path: str, static: bool = False) -> Template:
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

def load_ast(filename: str) -> ast.AST:
    """
    Loads root node of AST for a python file
    @param filename path to the file to load
    @return root ast node loaded from the file
    """
    with open(filename, 'r') as f:
        return ast.parse(f.read())

def get_classes(_ast: ast.AST) -> Generator[ast.ClassDef]:
    """
    Gets all class definitions that are children of the ast node
    @param _ast the ast node to search for functions in
    @return generator of class definition ast nodes
    """
    return (node for node in _ast.body if isinstance(node, ast.ClassDef))

def get_functions(_ast: ast.AST) -> Generator[ast.FunctionDef]:
    """
    Gets all function definitions that are children of the ast node
    @param _ast the ast node to search for functions in
    @return a tuple of function definition ast nodes
    """
    return (node for node in _ast.body if isinstance(node, ast.FunctionDef))

def parse_docstring(docstring: str, context: str) -> dict[str, str|list[str]]:
    """
    Parses parameters, thrown exception types, return values, and description from the docstring
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
                collection, result = Tag.parse(curr, context)
                if result is not None:
                    if collection not in parsed:
                        parsed[collection] = []
                    parsed[collection].append(result)
            curr = line
        else:
            curr += ' ' + line

    if curr != '':
        collection, result = Tag.parse(curr, context)
        if result is not None:
            if collection not in parsed:
                parsed[collection] = []
            parsed[collection].append(result)

    return parsed

# TODO: Review this and change if needed; lambda doesn't give very meaningful information,
# and it might be better to escape the string with str.encode('string_escape'), also
# should consider multi-line strings
def ast_object_to_str(ast_obj: ast.AST) -> str:
    if isinstance(ast_obj, ast.Lambda):
        return 'lambda ' + ','.join( arg.arg for arg in ast_obj.args.args )
    if isinstance(ast_obj, ast.Constant):
        return repr(ast_obj.value)
    return ''
