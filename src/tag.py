import sys
import os.path as path
import yaml

class Tag(object):
    """
    Represents a tag (prefixed with '@')
    """

    def __init__(self, obj):
        """
        @param obj the yaml object to parse the tag from.
               must have syntax and collection fields
        """
        items = obj['syntax'].split()
        self.maxsplit = len(items)-1
        self.tag = items[0]
        self.syntax = items[1:]
        self.collection = obj['collection']

    def parse(self, string):
        parts = string.split(maxsplit=self.maxsplit)
        if parts[0] != self.tag:
            return None
        # Don't need a dict for 1D tags
        if len(parts) == 2:
            return parts[1]

        tag = { self.syntax[i] : parts[i] for i in range(1, len(parts)) }
        return tag

    @staticmethod
    def load_tags(yaml_path, static=False):
        """
        @param yaml_path Path to the yaml file to load tags from
        @param static True to load the templates from the application path, False to load normally
        @return a list of tags from the yaml file
        """
        if static:
            root = path.dirname(sys.argv[0])
            yaml_path = path.join(root, yaml_path)
        with open(yaml_path, 'r') as f:
            obj = yaml.safe_load(f.read())
        tags = []
        for tag in obj:
            tags.append( Tag(tag) )
        return tags
