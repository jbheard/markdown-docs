import os
import utils
from tag import Tag
from doc_loader import get_data

def generate_docs(input_dir: str, output_dir: str):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # Load all python files in the directory (and subdirectories)
    files = utils.get_all_files(input_dir, '.py')

    Tag.load_tags('tags.yaml', True)

    # Convert all python files into AST objects
    classes, functions = [], []
    for file in files:
        _ast = utils.load_ast(file)
        classes.extend(utils.get_classes(_ast))
        functions.extend(utils.get_functions(_ast))

    # Create the readme, then create all subsequent pages
    data = get_data(classes, functions)
    readme_template = utils.load_template("../templates/readme.md", True)
    md = readme_template.render(data)
    with open(os.path.join(output_dir, 'README.md'), 'w') as file:
        file.write(md)

    # Create file for each class
    class_template = utils.load_template("../templates/class.md", True)
    for class_data in data['classes']:
        md = class_template.render(class_data)
        file_path = os.path.join(output_dir, class_data['name'] + '.md')
        with open(file_path, 'w') as file:
            file.write(md)


if __name__ == '__main__':
    from sys import argv, stderr
    if len(argv) < 3:
        print("Usage: {} input_dir output_dir".format(argv[0]), file=stderr)
        exit(1)

    generate_docs(argv[1], argv[2])
