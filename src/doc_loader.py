import ast
import os.path
from jinja2 import Template

import utils
from tag import Tag

# TODO: make title customizeable
def get_data(classes: list[ast.ClassDef], functions: list[ast.FunctionDef]) -> dict[str, str|list[str]]:
    data = { 'title' : 'Python Documentation', 'classes' : [], 'functions' : [] }
    for c in classes:
        c_data = get_class_data(c)
        data['classes'].append(c_data)

    for f in functions:
        data['functions'].append(get_function_data(f))
    return data

def get_class_data(_class: ast.ClassDef, context: str = '') -> dict[str, str|list[str]]:
    docstring = ast.get_docstring(_class) or ''
    context = f'{context}.{_class.name}'.strip('.')
    doc = utils.parse_docstring(docstring, context)
    doc['name'] = _class.name
    doc['href'] = _class.name + '.md'
    doc['functions'] = []

    for func in utils.get_functions(_class):
        f_data = get_function_data(func, _class.name)
        doc['functions'].append(f_data)
    return doc

def get_function_data(func: ast.FunctionDef, context: str = '') -> dict[str, str|list[str]]:
    docstring = ast.get_docstring(func) or ''
    context = f'{context}.{func.name}'.strip('.')
    doc = utils.parse_docstring(docstring, context)
    doc['name'] = func.name

    if len(func.args.args) > 0:
        if 'params' not in doc:
            doc['params'] = []
        args = func.args.args
        defaults = func.args.defaults
        for i in range(len(func.args.args)):
            arg = func.args.args[i].arg
            d_i = i - (len(args) - len(defaults))
            default = ''
            if d_i >= 0:
                default = utils.ast_object_to_str(defaults[d_i])

            found = False
            for i in range(len(doc['params'])):
                param = doc['params'][i]
                if param['name'] == arg:
                    param['default'] = default
                    found = True
            if not found:
                doc['params'].append({'name':arg,'description':'','default':default})

    return doc

def generate_docs(yaml_path: str, templates_dir: str, input_dir: str, output_dir: str):
    # Load all python files in the directory (and subdirectories)
    files = utils.get_all_files(input_dir, '.py')
    Tag.load_tags(yaml_path)

    # Convert all python files into AST objects
    classes, functions = [], []
    for path in files:
        with open(path, 'r') as f:
            _ast = ast.parse(f.read())
        classes.extend((node for node in _ast.body if isinstance(node, ast.ClassDef)))
        functions.extend((node for node in _ast.body if isinstance(node, ast.FunctionDef)))

    data = get_data(classes, functions)

    # Create the readme
    with open(os.path.join(templates_dir, 'readme.md'), 'r') as f:
        readme_template = Template(f.read())
    md = readme_template.render(data)
    with open(os.path.join(output_dir, 'README.md'), 'w') as file:
        file.write(md)

    # Create file for each class
    with open(os.path.join(templates_dir, 'class.md'), 'r') as f:
        class_template = Template(f.read())
    for class_data in data['classes']:
        md = class_template.render(class_data)
        file_path = os.path.join(output_dir, class_data['name'] + '.md')
        with open(file_path, 'w') as file:
            file.write(md)
