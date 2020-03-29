import sys
import ast
import utils
import os.path as path
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
        root = path.dirname(sys.argv[0])
        template_path = path.join(root, template_path)
    with open(template_path, 'r') as f:
        template = Template(f.read())
    return template

# TODO: make title customizeable
def make_readme_md(classes, functions, dir):
    template = load_template("../templates/readme.md", True)
    data = { 'title' : 'Python Documentation', 'classes' : [], 'functions' : [] }
    for c in classes:
        docstring = ast.get_docstring(c) or ''
        c_data = {'name' : c.name, 'href' : c.name + '.md'}
        doc = utils.parse_docstring(docstring, c.name)
        if len(doc['description']) > 0:
            c_data['description'] = doc['description']
        data['classes'].append(c_data)
    
    for f in functions:
        data['functions'].append(get_function_data(f))
    md = template.render(data)
    
    with open(path.join(dir, 'README.md'), 'w') as file:
        file.write(md)

def make_class_md(_class, dir):
    template = load_template("../templates/class.md", True)
    data = get_class_data(_class)
    md = template.render(data)
    with open(path.join(dir, _class.name + '.md'), 'w') as file:
        file.write(md)

def get_class_data(_class):
    docstring = ast.get_docstring(_class) or ''
    doc = utils.parse_docstring(docstring, _class.name)
    data = {'name':_class.name, 'href': _class.name+'.md', 'description':doc['description'], 'functions':[]}

    for func in utils.get_functions(_class):
        f_data = get_function_data(func, _class.name)
        data['functions'].append(f_data)
    return data

def get_function_data(func, context=''):
    docstring = ast.get_docstring(func) or ''
    doc = utils.parse_docstring(docstring, context + ' ' + func.name)
    data = { 'name': func.name, 'description': doc['description'] }

    if len(func.args.args) > 0:
        data['params'] = []
        args = func.args.args
        defaults = func.args.defaults
        for i in range(len(func.args.args)):
            arg = func.args.args[i].arg
            d_i = i - (len(args) - len(defaults))
            default = '' if d_i < 0 else utils.ast_object_to_str(defaults[d_i])
            description = '' if arg not in doc['params'] else doc['params'][arg]
            data['params'].append({'name':arg,'description':description,'default':default})

    if len(doc['throws']) > 0:
        data['throws'] = []
        for key, val in doc['throws'].items():
            data['throws'].append({'type':key, 'message':val})
    return data

