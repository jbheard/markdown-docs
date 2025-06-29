if __name__ == '__main__':
    from sys import argv, stderr
    if len(argv) < 3:
        print("Usage: {} input_dir output_dir".format(argv[0]), file=stderr)
        exit(1)

    import os
    from doc_loader import generate_docs

    root_dir = os.path.dirname(argv[0])
    tags_yaml_path = os.path.join(root_dir, 'tags.yaml')
    templates_dir = os.path.join(root_dir, '../templates/')
    input_dir = argv[1]
    output_dir = argv[2]

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    generate_docs(
        tags_yaml_path,
        templates_dir,
        input_dir,
        output_dir,
    )
