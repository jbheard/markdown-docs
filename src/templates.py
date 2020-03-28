import ast
import utils

LINK_WITH_DESCRIPTION = "**[{name}]({href})**: {description}\n\n"
LINK_NO_DESCRIPTION = "**[{name}]({href})**\n\n"

def make_readme_md( classes, functions ):
    md = "# Python Documentation\n\n## Classes\n\n"
    for c in classes:
        docstring = ast.get_docstring(c) or ''
        format_data = {'name' : c.name, 'href' : c.name + '.md'}
        doc = utils.parse_docstring(docstring, c.name)
        if len(doc['description']) > 0:
            format_data['description'] = doc['description']
            md += LINK_WITH_DESCRIPTION.format(**format_data)
        else:
            md += LINK_NO_DESCRIPTION.format(**format_data)

    md += "\n\n## Functions\n\n"
    for f in functions:
        md += get_function_md(f)
    
    with open('README.md', 'w') as file:
        file.write(md)


def make_class_md(_class):
    docstring = ast.get_docstring(_class) or ''
    doc = utils.parse_docstring(docstring, _class.name)
    md = '# {}\n\n'.format(_class.name)
    if len(doc['description']) > 0:
        md += doc['description'] + '\n\n'

    md += '## Functions\n\n'
    for func in utils.get_functions(_class):
        md += get_function_md(func, _class.name)
    
    with open(_class.name + '.md', 'w') as file:
        file.write(md)


def get_function_md(func, context=''):
    docstring = ast.get_docstring(func) or ''
    doc = utils.parse_docstring(docstring, context + ' ' + func.name)
    md = '### {}\n\n'.format(func.name)
    if len(doc['description']) > 0:
        md += doc['description'] + '\n\n'
    if len(func.args.args) > 0:
        args = func.args.args
        defaults = func.args.defaults
        md += '#### Parameters\n'
        md += 'name | description | default\n---|---|---\n'
        for i in range(len(func.args.args)):
            arg = func.args.args[i].arg
            d_i = i - (len(args) - len(defaults))
            default = '' if d_i < 0 else defaults[d_i]
            description = '' if arg not in doc['params'] else doc['params'][arg]
            md += "{} | {} | {}\n".format(arg, description, default)
        md += "\n\n"
    if len(doc['throws']) > 0:
        md += "#### Throws\n\n"
        for key, val in doc['throws'].items():
            md += "**{}** : {}  \n".format(key, val)
        md += '\n\n'
    return md
