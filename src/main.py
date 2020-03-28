import os
import utils
import templates

if __name__ == '__main__':
    from sys import argv, stderr
    if len(argv) < 2:
        print("Usage: {} input_dir output_dir".format(argv[0]), file=stderr)
        exit(1)

    # Load all python files in the directory (and subdirectories)
    output = argv[2]
    if not os.path.isdir(output):
        os.mkdir(output)
    files = utils.get_all_files(argv[1], '.py')

    # Convert all python files into AST objects
    classes = []
    functions = []
    for file in files:
        _ast = utils.load_ast(file)
        classes.extend(utils.get_classes(_ast))
        functions.extend(utils.get_functions(_ast))

    # Create the readme, then create all subsequent 
    templates.make_readme_md(classes, functions, output)
    for c in classes:
        templates.make_class_md(c, output)
