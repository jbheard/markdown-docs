import utils
import templates

if __name__ == '__main__':
    from sys import argv, stderr
    if len(argv) < 2:
        print("Usage: {} file_path".format(argv[0]), file=stderr)
        exit(1)

    # Load all python files in the directory (and subdirectories)
    files = utils.get_all_files(argv[1], '.py')
    classes = []
    functions = []
    for file in files:
        _ast = utils.load_ast(file)
        classes.extend(utils.get_classes(_ast))
        functions.extend(utils.get_functions(_ast))
    
    templates.make_readme_md(classes, functions)
    for c in classes:
        templates.make_class_md(c)
