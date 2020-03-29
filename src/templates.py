import sys, os, ast
import utils
from jinja2 import Template

LINK_WITH_DESCRIPTION = "**[{name}]({href})**: {description}\n\n"
LINK_NO_DESCRIPTION = "**[{name}]({href})**\n\n"

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

# TODO: make title customizeable
def get_data(classes, functions, dir):
    template = load_template("../templates/readme.md", True)
    data = { 'title' : 'Python Documentation', 'classes' : [], 'functions' : [] }
    for c in classes:
        c_data = get_class_data(c)
        data['classes'].append(c_data)
    
    for f in functions:
        data['functions'].append(get_function_data(f))
    return data

def get_class_data(_class):
    docstring = ast.get_docstring(_class) or ''
    doc = utils.parse_docstring(docstring, _class.name)
    doc['name'] = _class.name
    doc['href'] = _class.name + '.md'
    doc['functions'] = []

    for func in utils.get_functions(_class):
        f_data = get_function_data(func, _class.name)
        doc['functions'].append(f_data)
    return doc

def get_function_data(func, context=''):
    docstring = ast.get_docstring(func) or ''
    doc = utils.parse_docstring(docstring, context + ' ' + func.name)
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

