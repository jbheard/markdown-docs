import os, ast
from tag import Tag

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
                filenames.append( os.path.join(root, name).replace(os.path.sep, '/') )
    return filenames

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
