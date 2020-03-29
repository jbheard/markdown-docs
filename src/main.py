import os
import utils
from tag import Tag
from doc_loader import get_data

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

    Tag.load_tags('tags.yaml', True)

    # Convert all python files into AST objects
    classes = []
    functions = []
    for file in files:
        _ast = utils.load_ast(file)
        classes.extend(utils.get_classes(_ast))
        functions.extend(utils.get_functions(_ast))

    # Create the readme, then create all subsequent 
    data = get_data(classes, functions, output)
    readme_template = utils.load_template("../templates/readme.md", True)
    md = readme_template.render(data)
    with open(os.path.join(output, 'README.md'), 'w') as file:
        file.write(md)

    # Create file for each class
    class_template = utils.load_template("../templates/class.md", True)
    for class_data in data['classes']:
        md = class_template.render(class_data)
        file_path = os.path.join(output, class_data['name'] + '.md')
        with open(file_path, 'w') as file:
            file.write(md)
