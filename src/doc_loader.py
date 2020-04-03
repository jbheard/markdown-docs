import sys, os, ast
import utils

# TODO: make title customizeable
def get_data(classes, functions, dir, extension='.md'):
    data = { 'title' : 'Python Documentation', 'classes' : [], 'functions' : [] }
    for c in classes:
        c_data = get_class_data(c, extension)
        data['classes'].append(c_data)
    
    for f in functions:
        data['functions'].append(get_function_data(f))
    return data

def get_class_data(_class, extension='.md'):
    docstring = ast.get_docstring(_class) or ''
    doc = utils.parse_docstring(docstring, _class.name)
    doc['name'] = _class.name
    doc['href'] = _class.name + extension
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

